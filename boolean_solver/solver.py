#!/usr/bin/env python

"""This is the main file. Calls QM algorithm and code generation functions."""

import inspect
from util import *
from conditions import *
from code_generator import *
import qm
#  TODO: from boolean_solver import solver as production_solver

__author__ = 'juan pablo isaza'


# TODO: do the comment section of functions.


def solve_boolean():
    """
    This defines a Decorator, that will wrap the generated functions.
    :return: boolean value of generated function.
    """
    def wrap(f):

        def wrapped_f(*args):
            #  TODO: run test and implement and run function.
            return f(*args)

        # Meta data transfer enables introspection of decorated functions.
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


def from_table_to_ones(table):
    """
    Gets the ones as a list of strings from a truth table like set, containing tuples.
    :param table: truth table
    :return: set containing bits.
    """
    ones = []
    for row in table:

        # case 1: when the output is explicit.
        if Conditions.is_explicit(row):
            if row[1]:  # only do it for true outputs.# TODO change for non booleans.
                ones.append(''.join(list(map(from_bool_to_bit, list(row[0])))))

        else:  # case 2: The output is a implicit True. inputs are in the row.
            ones.append(''.join(list(map(from_bool_to_bit, list(row)))))

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
        if isinstance(row[0], tuple):
            r = eval(replace_expression(expression, inputs, row[0]))
            test_class.assertEqual(r, row[1])
        else:
            r = eval(replace_expression(expression, inputs, row))
            test_class.assertEqual(r, True)


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
    def __init__(self, expressions, implementation, callable_function, conditions):
        self.expressions = expressions
        self.implementation = implementation
        self.callable_function = callable_function
        self.conditions = conditions


def alter_file(line_number, input_file_list, implementation, input_path):
    """
    Changes source file, when valid implementation found.
    :param line_number: of source.
    :param input_file_list: contains all lines of source.
    :param implementation: the new function.
    :param input_path: source file path.
    :return: void
    """
    source = get_function_code(line_number, input_file_list)

    input_file_list = input_file_list[:line_number] + implementation + input_file_list[line_number + len(source):]
    rewrite_file(input_path, input_file_list)


def get_empty_solution(callable_function, conditions):
    return Solution(expressions=[],
                    implementation=[],
                    callable_function=callable_function,
                    conditions=conditions)


def add_default_return(definition, tables, implementation):
    """
    Modify source code to include a default return if no True key is present.
    :param definition: function def
    :param tables: dict with tables.
    :param implementation: source code
    :return: source code
    """
    indent = re.search(INDENT, definition).group()
    if not(has_true_key(tables)):
        implementation = implementation + ['', indent + '    return False']
    return implementation


def return_solution(unittest, f, conditions):
    """
    Solves the riddle, Writes it and tests it.
    :param conditions: condition or object or partial truth table (explicit, implicit or mix).
    :return: True for successful operation, False if not.
    """
    f_path = get_function_path(f)
    file_code = read_file(f_path)
    f_line = get_function_line_number(f, file_code)

    # enters only if the function source code was found.
    if f_line > 0 and get_signature(file_code[f_line]):

        definition = file_code[f_line]
        inputs = get_function_inputs(f)

        # init variables
        implementation = INITIAL_IMPLEMENTATION
        tables = get_truth_tables(conditions, inputs)
        expressions = []

        for the_output, table in tables.iteritems():

            expression = get_function_expression(table, inputs)
            if len(expression) > 0:

                # TODO: change testing to include the whole function.
                # test, before writing.
                test_expression(unittest, expression, table, inputs)
                expressions.append(expression)

                implementation = add_code_to_implementation(current_implementation=implementation,
                                                            bool_expression=expression,
                                                            definition=definition,
                                                            the_output=the_output)

        implementation = add_default_return(definition, tables, implementation)

        alter_file(f_line, file_code, implementation, f_path)
        print "Solved and tested " + f.__name__

        return Solution(expressions=expressions,
                        implementation=implementation,
                        callable_function=f,
                        conditions=conditions)

    return get_empty_solution(f, conditions)


def reload_function(f):
    """
    Reloads the function, to make sure that any metadata is up to date (such as func_code)
    :param f: function
    :return: updated function
    """
    module = inspect.getmodule(f)
    reload(module)
    # TODO: find any method anywhere within the module.
    return getattr(module, f.__name__)


def execute(unittest, callable_function, conditions):
    """
    Solves the riddle, Writes it and tests it.
    :param unittest: the current test being run eg: 'self'.
    :param callable_function: the function to be coded.
    :param conditions: condition or object or partial truth table (explicit, implicit or mix).
    :return: Solution object, empty object if operation unsuccessful.
    """
    # input validation
    if not valid_function(callable_function) or not valid_conditions(conditions):
        return get_empty_solution(callable_function, conditions)

    callable_function = reload_function(callable_function)
    f_path = get_function_path(callable_function)

    if not os.path.exists(f_path):
        return get_empty_solution(callable_function, conditions)

    return return_solution(unittest=unittest,
                           f=callable_function,
                           conditions=conditions)
