__author__ = 'juan pablo isaza'
import re
import warnings
import qm

from util import *


FUNCTION_PATTERN = re.compile(r"(\w+)\(\s*(\w+)(,\s*(\w+))+\)")
DEF_PATTERN = re.compile(r"\s*def\s*")
FUNCTION_PATTERN_DEFINITION = re.compile(DEF_PATTERN.pattern + FUNCTION_PATTERN.pattern)
WORD_PATTERN = re.compile(r"\w+")
INDENT = re.compile(r"^\s*")
DECORATOR = re.compile(r"@.*\.?solve_boolean\(\)")

# TODO: do the comment section of functions.


def solve_boolean():
    """
    This defines a Decorator, that will wrap the generated functions.
    :return: boolean value of generated function.
    """
    def wrap(f):

        def wrapped_f(*args):
            #  TODO: run test and implement and run function.
            """
            if hasattr(output.generated_code, f.__name__):
                function_to_call = getattr(output.generated_code, f.__name__)
                return function_to_call(*args)
            else:
                warnings.warn('function name: ' + str(f.__name__) +
                              ' is still a mock function, please run test to generate it')
            """

            return f(*args)

        wrapped_f.__name__ = f.__name__
        wrapped_f.__module__ = f.__module__
        wrapped_f.internal_func_code = f.func_code
        return wrapped_f
    return wrap


def execute_mc_algorithm(ones):
    """
    Quine McCluskey algorithm.
    outputs the minimal boolean expression. Assumes that all none ones have a False output.
    :param ones: input combinations for which output is true
    :return: set containing lists of boolean expressions encoded as strings.
    Where: '1' = boolean ,'0' = not(boolean), '-' = don't care, '^^' = boolean0 ^ boolean1
    Example: set('1-','-0') = bit0 or not bit1
    """
    # TODO: cannot solve ones = ['00'] or a not(or(b0,b1))
    # TODO: change to True, add XOR logic
    qm_obj = qm.QuineMcCluskey(use_xor=False)
    return qm_obj.simplify_los(ones, set([]))


def translate_to_python_expression(bool_variables, mc_output):
    """
    Converts the algorithm output to friendlier python code.
    :param bool_variables: array with the names of the boolean inputs.
    :param mc_output: set containing strings. see "execute_mc_algorithm" for details.
    :return: python boolean expression
    """
    final_bool = ""

    for i, str_bits in enumerate(mc_output):

        factor = ""

        if i > 0:  # when more than one element on list, join by "or"
            final_bool += " or "

        for j, c in enumerate(str_bits):

            if string_has_bits_for_and(str_bits, j):
                factor += " and "

            if c == "1":
                factor += bool_variables[j]

            if c == "0":
                factor += "not " + bool_variables[j]

        final_bool += factor

    return final_bool


def get_function_name(signature):
    """
    Given function signatures gets the name of the function.
    :param signature: exp: sum(a,b)
    :return: name as a string.
    """
    word_match = re.findall(WORD_PATTERN, signature)
    return word_match[0]


def get_function_inputs(signature):
    """
    Given function signatures gets the name of the function.
    :param signature: exp: sum(a,b)
    :return: input names on a list.
    """
    word_match = re.findall(WORD_PATTERN, signature)
    return word_match[1:]


def get_signature(definition):
    """
    Gets the signature of a function given the definition ie: from:'    def sum(a, b):  #bla bla bla' to 'sum(a,b)'
    :param definition:
    :return: string signature.
    """
    return re.search(FUNCTION_PATTERN, definition).group()


def get_function_expression(table, inputs):
    """
    Get boolean expression. Can return empty string.
    solution provided by mc algorithm.
    :param table: truth table.
    :return: string with boolean expression.
    """
    ones = from_table_to_ones(table)
    if len(ones) > 0:
        mc_output = execute_mc_algorithm(ones)
        return translate_to_python_expression(inputs, mc_output)
    else:
        return ''


def get_function_implementation(expression, definition):
    """
    Given definition and expression gets the function implementation.
    :param expression: truth table.
    :param definition:   def function(input1, input2, ...).
    :return: string list with implementation.
    """
    signature = get_signature(definition)
    indent = re.search(INDENT, definition).group()
    if expression and len(expression) > 0:
        return [indent + "def " + signature + ":", indent + "    return " + expression]
    else:
        warnings.warn('Function: ' + signature + ' has no boolean expression; cannot be implemented', UserWarning)
        return []


def from_table_to_ones(table):
    """
    Gets the ones as a list of strings from a truth table like set, containing tuples.
    :param table: truth table
    :return: set containing bits.
    """
    ones = []
    for row in table:
        if row[1]:  # only do it for true outputs.
            ones.append(''.join(list(map(from_bool_to_bit, list(row[0])))))

    return set(ones)


def test_expression(test_class, expression, table, inputs):
    """
    Tests function for all table outcomes.
    :param test_class: the self in the unittest.
    :param expression: boolean.
    :param table: truth table.
    :param inputs: name of variables.
    :return: pass or not pass
    """
    for row in table:
        r = eval(replace_expression(expression, inputs, row[0]))
        test_class.assertEqual(r, row[1])


def replace_expression(expression, inputs, values):
    """
    Replace variables for boolean values.
    :param expression: boolean.
    :param inputs: variable names.
    :param values:
    :return: expression that can be evaluated.
    """
    for n, var in enumerate(inputs):
            regex = "(^|\s+)" + var + "(\s+|$)"
            expression = re.sub(re.compile(regex), " " + str(values[n]) + " ", expression)
    return expression


class Solution:
    """
    Contains the data describing the solution to the puzzle.
    """
    def __init__(self, expression, implementation, callable_function, table):
        self.expression = expression
        self.implementation = implementation
        self.callable_function = callable_function
        self.table = table


def alter_file(line_number, input_file_list, implementation, input_path):
    """
    Changes source file, when valid implementation found.
    :param line_number: of source.
    :param input_file_list: contains all lines of source.
    :param implementation: the new function.
    :param input_path: source file path.
    :return: void
    """
    input_file_list[line_number] = implementation[0]
    input_file_list[line_number+1] = implementation[1]
    rewrite_file(input_path, input_file_list)


def execute(unittest_object, callable_function, table):
    """
    Solves the riddle, Writes it and tests it.
    :param table: a truth table, or at least the rows where the output is True.
    :return: True for successful operation, False if not.
    """
    input_path = get_function_path(callable_function)
    input_file_list = read_file(input_path)
    expression = ''
    implementation = []

    # iterate over the file and find annotation and definition.
    line_before = ""
    for line_number, line in enumerate(input_file_list):

        match_dec = re.search(DECORATOR, line_before)
        match_def = re.search(FUNCTION_PATTERN_DEFINITION, line)

        if match_dec and match_def:

            decorator = match_dec.group()
            definition = match_def.group()

            if decorator and definition:

                signature = get_signature(definition)

                if signature and get_function_name(signature) == callable_function.__name__:

                    inputs = get_function_inputs(signature)
                    expression = get_function_expression(table, inputs)

                    # test, before writing.
                    test_expression(unittest_object, expression, table, inputs)

                    implementation = get_function_implementation(expression, definition)

                    alter_file(line_number, input_file_list, implementation, input_path)

                    break

        # will not count space lines.
        if line.strip() != "":
            line_before = line

    print "Solved and tested " + callable_function.__name__

    return Solution(expression=expression,
                    implementation=implementation,
                    callable_function=callable_function,
                    table=table)