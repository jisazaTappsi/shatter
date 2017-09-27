import copy
import signal
import itertools

from sympy.logic import POSform
import sympy
import pyeda.inter as pyEDA

from shatter import float_input_helper as helper
from shatter.machine_learning.labeled_data import from_dict_to_data_frame
from shatter.constants import *


def add_empty_columns(df, variables):
    for var in variables:
        df[var] = [None for _ in range(len(df))]
    return df


def add_boolean_table(df, variables, var_name):
    """
    Fills in values for the table of new comparison variables.
    :param df: DataFrame
    :param variables: all variables that are treated as boolean, but are comparison equations.
    :param var_name: one of the original variables.
    :return: modified DataFrame
    """
    for idx, _ in enumerate(df.iterrows()):
        for code in variables:
            input_var = df.loc[idx, var_name]

            # This is a bit complicated here:
            # STEP 1: First assigns a value to a variable
            exec('{} = {}'.format(var_name, input_var))

            # STEP 2: Then executes a comparison on the assigned value from the previous step, and assign result to df.
            df.loc[idx, code] = eval(str(code))

    return df


def get_qm_inputs(df):
    """
    Gets the inputs to the final QM problem(the one done upon the newly defined comparison variables).
    Also removes the output column.
    :param df: same old DataFrame
    :return: outputs a list containing tuples with int values {0, 1}
    """
    df.drop([KEYWORDS[OUTPUT]], inplace=True, axis=1)
    return [tuple([int(e) for e in inputs]) for inputs in df.values.tolist()]


def get_positive_negative_and_dont_care_sets(df):
    """
    The product set of length n Boolean sequences eg: {(0, 0), (0, 1), (1, 0), (1, 1)} for n=2
    Can be divided into 3 sets:
    1. Set that should output a True value
    2. Set that should output a False value
    3. Set which output doesn't matter.(don't care)
    :param df: DataFrame with True and False outcomes
    :return: A tuple with 3 sets:
    1. True outcomes
    2. Don't care
    """

    qm_outputs = copy.copy(df[KEYWORDS[OUTPUT]])
    qm_inputs = get_qm_inputs(df)

    # Takes length of first element.
    length_n = len(qm_inputs[0])

    # gets length n product set.
    all_permutations = {e for e in itertools.product(range(2), repeat=length_n)}

    min_terms = {i for i, o in zip(qm_inputs, qm_outputs) if o}
    zeroes = {i for i, o in zip(qm_inputs, qm_outputs) if not o}

    # removes all min_terms and zeroes, inplace
    [all_permutations.remove(x) for x in min_terms | zeroes]

    dontcares = all_permutations

    return min_terms, dontcares


def get_symbol_list(df):
    """
    :param df: DataFrame
    :return: List with symbols for Sympy to solve.
    """
    symbols_str = ' '.join([str(comparison_obj).replace(' ', '') for comparison_obj in df.columns.values])

    symbols_var = sympy.symbols(symbols_str)
    if len(df.columns.values) > 1:  # has more than an element
        return [var for var in symbols_var]
    else:
        return [symbols_var]


def print_pyeda_expression(pyeda_exp):
    """
    Print the right stuff. Has to traverse tree see:
    http://pyeda.readthedocs.io/en/latest/expr.html
    :param pyeda_exp:
    :return: string
    """

    operation = pyeda_exp.ASTOP

    if operation == 'lit':
        return str(pyeda_exp).replace('~', 'not ')

    expressions = pyeda_exp.xs

    expression = ''
    for idx, exp in enumerate(expressions):

        if idx > 0:
            expression += ' ' + operation + ' ' + print_pyeda_expression(exp)
        else:
            expression = print_pyeda_expression(exp)

    return expression


def get_pyeda_out_string(df, n):
    """
    Gets a string that is the output of a truth table, see a library pyEDA example.
    :param df: DataFrame with minterms rows (False and True values).
    :param n: size of the problem
    :return: string with '0', '1', '-' values.
    """

    # all outputs are assumed to be don't cares.
    out = '-'*(2**n)

    for i, row in df.iterrows():

        # calculates a binary number, and uses it as the index of the out string.
        my_bin = ''
        for key, value in row.iteritems():
            if key != KEYWORDS[OUTPUT]:
                my_bin += str(int(value))

        idx = int(my_bin, 2)

        value = str(int(row[KEYWORDS[OUTPUT]]))

        tmp_list = list(out)
        tmp_list[idx] = value
        out = ''.join(tmp_list)

    return out


def get_pyEDA_expression(df):
    """
    Gets the expression with the Espresso heuristic algorithm.
    Works when QM fails for problems with 7 variables or larger.
    :param df: pandas DataFrame
    :return: string with expression.
    """
    columns = list(df.columns.values)

    # size of the problem
    n = len(columns)-1

    # gets all boolean combinations for a number of variables.
    x = pyEDA.ttvars('x', n)

    out = get_pyeda_out_string(df, n)

    truth_table = pyEDA.truthtable(x, out)
    pyeda_expression = pyEDA.espresso_tts(truth_table)[0]

    expression = print_pyeda_expression(pyeda_expression)
    for i, s in enumerate(reversed(columns[1:])):
        expression = expression.replace('x[{}]'.format(i), str(s))

    return expression


def clean_up_dataframe(df, percent_cut, input_ranges):

    # yields Comparison objects.
    comparisons = list(df.columns.values)
    comparisons.remove(KEYWORDS[OUTPUT])

    for comparison in comparisons:

        my_range = input_ranges[comparison.get_input()]
        if comparison.should_be_removed(my_range, percent_cut):
            df.drop(comparison, inplace=True, axis=1)

    return df


class TimeoutException(Exception):
    """Custom exception class"""
    pass


def timeout_handler(signum, frame):
    """Custom signal handler"""
    raise TimeoutException


def solve_big_table(df, input_ranges):
    """
    Tries several times to solve the problem, each time it fails (waiting more than 10 seconds) it relaxes constraints
    and makes the problem a bit easier, although it might not be exact.
    :param df: DataFrame.
    :param input_ranges: dictionary with ranges for each variable.
    :return: string with expression
    """

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

    # initially accepts every nuance.
    exp = ''
    cut_percent = 0
    for i in range(5):
        # Start the timer. Once 10 seconds are over, a SIGALRM signal is sent.
        signal.alarm(10)
        # This try/except loop ensures that
        #   you'll catch TimeoutException when it's sent.
        try:
            exp = get_pyEDA_expression(df)
        except TimeoutException:

            # removes intervals shorter than this number
            cut_percent += 0.1
            df = clean_up_dataframe(df, cut_percent, input_ranges)
            continue
        except MemoryError:
            # removes intervals shorter than this number
            cut_percent += 0.1
            df = clean_up_dataframe(df, cut_percent, input_ranges)
            continue
        else:
            # Reset the alarm
            signal.alarm(0)

    return exp


def get_float_classification(binary_tables, all_inputs):
    """
    Outer function calculating expression when:
    1. Inputs real numbers(eg the set R in mathematics)
    2. Output is binary.
    :param binary_tables: This a type of dictionary with 2 keys only: boolean values True and False.
    :param all_inputs: all possible inputs to the problem (either direct or indirectly implied).
    :return: a expression summarizing efficiently the hypothesis.
    """

    df, input_ranges = get_data_frame(binary_tables, all_inputs)

    if len(list(df.columns.values)) < 8:  # Uses exact solution with Quine McCluskey
        min_terms, dont_cares = get_positive_negative_and_dont_care_sets(df)
        symbols_list = get_symbol_list(df)
        exp = POSform(symbols_list, min_terms, dont_cares)

        # TODO: this expression are correct but none PEP-8 complaint
        exp = str(exp).replace('and', ' and ').replace('~', 'not ').replace('|', 'or').replace('&', 'and')
    else:  # Big problem uses Heuristic Espresso.
        exp = solve_big_table(df, input_ranges)

    return exp


def get_dataframe_duplicates(df, an_input, from_idx=0):
    """
    Given a DataFrame that can have same repeated values for the "an_input" column, but different output.
    Then 2 DataFrames have to be considered by swapping rows.
    This is done with a much more efficient algorithm.
    :param df: DataFrame
    :param an_input: string with a column of the DataFrame
    :param from_idx: searches for duplicates after this DataFrame index.
    :return: Best DataFrame candidate
    """

    values = list(df[an_input])
    outputs = list(df[KEYWORDS[OUTPUT]])

    # finds duplicates
    last_value = None
    last_output = None

    # Takes a slice of the zipped list.
    zipped_list = [(v, o) for v, o in zip(values, outputs)][from_idx:]

    best_df = df
    min_jumps = get_compactness(df)
    for idx, (value, output) in enumerate(zipped_list):

        # adds the missing value.
        idx += from_idx

        # Is there a duplicate?
        if value == last_value and output != last_output:

            # make completely new DataFrame
            new_df = best_df.copy()

            # Swap DataFrame rows.
            new_df.iloc[idx-1], new_df.iloc[idx] = new_df.iloc[idx].copy(), new_df.iloc[idx-1].copy()

            jumps = get_compactness(new_df)
            if jumps < min_jumps:
                best_df = new_df
                min_jumps = jumps

        last_value = value
        last_output = output

    return best_df


def get_compactness(df):
    """
    Number of changes from 0 to 1 or vice versa, when iterating over the DataFrame
    :param df: DataFrame
    :return: number of jumps, or measure of compactness.
    """
    jumps = 0
    last_output = None
    for _, row in df.iterrows():
        output = row[KEYWORDS[OUTPUT]]
        if last_output is not None and output != last_output:
            jumps += 1

        last_output = output

    return jumps


def get_data_frame(binary_tables, all_inputs):
    """
    Gets a data frame that needs QM reduction and further logic.
    Also removes the all_inputs from the DataFrame.
    :param binary_tables: contains a tables with True and False outputs.
    :param all_inputs: columns
    :return: Pandas DataFrame.
    """

    columns = all_inputs + [KEYWORDS[OUTPUT]]
    df = from_dict_to_data_frame(binary_tables, columns)

    for an_input in all_inputs:

        df = df.sort([an_input], ascending=[1])

        #import time
        #start = time.time()
        best_df = get_dataframe_duplicates(df, an_input)
        #print('get_dataframe_duplicates for {}: {}'.format(an_input, time.time() - start))

        # only takes unique values.
        variables = set(helper.get_variables(best_df, an_input))

        #start = time.time()
        df = add_empty_columns(df, variables)
        #print('add_empty_column for {}: {}'.format(an_input, time.time() - start))

        #start = time.time()
        df = add_boolean_table(df, variables, an_input)
        #print('add_boolean_table for {}: {}'.format(an_input, time.time() - start))

    # before dropping all_inputs columns, will record their range.
    input_ranges = {}
    for the_input in all_inputs:
        input_ranges[the_input] = [min(list(df[the_input])), max(list(df[the_input]))]

    df.drop(all_inputs, inplace=True, axis=1)
    df.drop_duplicates(keep='first', inplace=True)

    return df, input_ranges
