import copy
import itertools

from sympy.logic import POSform
from sympy import symbols

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
            result = eval(code)
            df.loc[idx, code] = result

    return df


def get_qm_inputs(df, all_inputs):
    """
    Gets the inputs to the final QM problem(the one done upon the newly defined comparison variables).
    Also removes the all_inputs and output from the DataFrame (not so desirable side-effect).
    :param df: same old DataFrame
    :param all_inputs: problem inputs.
    :return: outputs a list containing tuples with int values {0, 1}
    """
    columns = all_inputs + [KEYWORDS[OUTPUT]]
    df.drop(columns, inplace=True, axis=1)
    return [tuple([int(e) for e in inputs]) for inputs in df.values.tolist()]


def get_positive_negative_and_dont_care_sets(df, all_inputs):
    """
    The product set of length n Boolean sequences eg: {(0, 0), (0, 1), (1, 0), (1, 1)} for n=2
    Can be divided into 3 sets:
    1. Set that should output a True value
    2. Set that should output a False value
    3. Set which output doesn't matter.(don't care)
    :param df: DataFrame with True and False outcomes
    :param all_inputs: problem inputs
    :return: A tuple with 3 sets:
    1. True outcomes
    2. Don't care
    """

    qm_outputs = copy.copy(df[KEYWORDS[OUTPUT]])
    qm_inputs = get_qm_inputs(df, all_inputs)

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
    symbols_str = ' '.join([e.replace(' ', '') for e in df.columns.values])

    symbols_var = symbols(symbols_str)
    if len(df.columns.values) > 1:  # has more than an element
        return [var for var in symbols_var]
    else:
        return [symbols_var]


def get_float_classification(binary_tables, all_inputs):
    """
    Outer function calculating expression when:
    1. Inputs real numbers(eg the set R in mathematics)
    2. Output is binary.
    :param binary_tables: This a type of dictionary with 2 keys only: boolean values True and False.
    :param all_inputs: all possible inputs to the problem (either direct or indirectly implied).
    :return: a expression summarizing efficiently the hypothesis.
    """

    df = get_data_frame(binary_tables, all_inputs)

    min_terms, dontcares = get_positive_negative_and_dont_care_sets(df, all_inputs)

    symbols_list = get_symbol_list(df)
    exp = POSform(symbols_list, min_terms, dontcares)
    exp = str(exp).replace('and', ' and ').replace('~', 'not ').replace('|', 'or').replace('&', 'and')
    # TODO: this expression are correct but none PEP-8 complaint
    return exp


def get_dataframe_duplicates_recursive(df, an_input, from_idx=0):
    """
    Given a DataFrame that can have same repeated values for the "an_input" column, but different output.
    Then 2 DataFrames have to be considered by swapping rows.
    :param df: DataFrame
    :param an_input: string with a column of the DataFrame
    :param from_idx: searches for duplicates after this DataFrame index.
    :return: List of possible DataFrame orderings. Called here duplicates.
    """
    # At least the df is its same duplicate
    duplicates = [df]

    values = list(df[an_input])
    outputs = list(df[KEYWORDS[OUTPUT]])

    # finds duplicates
    last_value = None
    last_output = None

    # Takes a slice of the zipped list.
    zipped_list = [(v, o) for v, o in zip(values, outputs)][from_idx:]

    for idx, (value, output) in enumerate(zipped_list):

        # adds the missing value.
        idx += from_idx

        # Is there a duplicate?
        if value == last_value and output != last_output:

            # make completely new DataFrame
            new_df = df.copy()

            # Swap DataFrame rows.
            new_df.iloc[idx-1], new_df.iloc[idx] = new_df.iloc[idx].copy(), new_df.iloc[idx-1].copy()

            duplicates += get_dataframe_duplicates_recursive(new_df, an_input, from_idx=idx)

        last_value = value
        last_output = output

    return duplicates


def get_dataframe_duplicates(df, an_input):
    """
    Given a DataFrame that can have same repeated values for the "an_input" column, but different output.
    Then 2 DataFrames have to be considered by swapping rows.
    :param df: DataFrame
    :param an_input: a column name
    :return: List containing all DataFrames to consider.
    """
    return get_dataframe_duplicates_recursive(df, an_input)


def choose_compact_dataframe(df_list):
    """
    Given a list of DataFrames will choose the one with the least number of 'ups' and 'downs'.
    :param df_list: DataFrame list
    :return: DataFrame
    """

    min_jumps = 1000000000
    selected_df = None
    for df in df_list:

        # is the number of changes from 0 to 1 or vice versa, when iterating over the DataFrame
        jumps = 0
        last_output = None
        for _, row in df.iterrows():
            output = row[KEYWORDS[OUTPUT]]
            if last_output is not None and output != last_output:
                jumps += 1

            last_output = output

        if jumps < min_jumps:
            min_jumps = jumps
            selected_df = df

    return selected_df


def get_data_frame(binary_tables, all_inputs):
    """
    Gets a data frame that needs QM reduction and further logic.
    :param binary_tables: contains a tables with True and False outputs.
    :param all_inputs: columns
    :return: Pandas DataFrame.
    """
    columns = all_inputs + [KEYWORDS[OUTPUT]]
    df = from_dict_to_data_frame(binary_tables, columns)

    for an_input in all_inputs:

        df = df.sort([an_input], ascending=[1])

        df_list = get_dataframe_duplicates(df, an_input)

        best_df = choose_compact_dataframe(df_list)

        variables = []

        #for df in df_list:
        #    variables += helper.get_variables(df, an_input)
        variables += helper.get_variables(best_df, an_input)

        # only takes unique values.
        variables = set(variables)

        df = add_empty_columns(df, variables)
        df = add_boolean_table(df, variables, an_input)

    return df


#if __name__ == '__main__':
#    my_test()
