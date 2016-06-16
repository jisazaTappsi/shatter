#!/usr/bin/env python

"""Implements the functions to test generated code."""
import traceback

from boolean_solver.code import Code
from boolean_solver.util.helpers import *

__author__ = 'juan pablo isaza'


def get_eval_code(args_str, function):
    """
    Invokes function below implementation.
    :param args_str: eg: 'a=True, b=False'
    :param function: to be tested
    :return: code to run.
    """
    return function.__name__ + '(' + args_str + ')'


def get_all_possible_inputs(inputs):
    """
    List comprehensions looping to create all possible binary combinations
    of inputs.
    :param inputs: the input list
    :return: a set containing all possible combinations.
    """
    n = len(inputs)
    return set([tuple([bool(int(c)) for c in bin(x)[2:].rjust(n, '0')]) for x in range(2**n)])


def get_used_inputs(tables):
    """
    List comprehensions are used to get all tuples.
    :param tables: the variable in processed_conditions.
    :return: a set with all used tuples.
    """
    return set([item for k, set_v in tables.iteritems() for item in set_v])


def get_inputs_with_default_output(inputs, tables):
    """
    Gets a set with all tuples going to default value.
    :param inputs: function ins.
    :param tables: as in processed_conditions.
    :return: tuples that output default value.
    """
    all_tuples = get_all_possible_inputs(inputs)
    used_tuples = get_used_inputs(tables)
    return all_tuples.difference(used_tuples)


def print_inputs_of_tuple(a_tuple):
    """
    Prints parts of the tuple which have inputs.
    :param a_tuple: a tuple
    :return: str
    """
    result = ''.join([str(e) + ', ' if not isinstance(e, Code) else '' for e in a_tuple])
    return result[:-2]


def run_single_test(test_class, a_tuple, solution, expected_value):
    """
    Test for a single input values.
    :param test_class: the unittest instance
    :param a_tuple: either dict() or tuple with inputs.
    :param solution: obj
    :return: passes, not passes, or cannot be tested by lack of context :(
    """

    function_call_code = get_eval_code(print_inputs_of_tuple(a_tuple), solution.function)

    try:
        exec "\n".join(solution.implementation)
        given_out = eval(function_call_code)

    except:
        w_str = "Cannot test function, probably lack of context, exception is: "
        warnings.warn(w_str, UserWarning)
        traceback.print_exc()
    else:
        test_class.assertEqual(given_out, expected_value)


def has_code_args(tables):
    """
    Returns True if any argument in the tables is a Code obj.
    :param tables: dict with keys as outputs and sets of tuples as dict values.
    :return: bool
    """
    for k, v_set in tables.iteritems():
        for a_tuple in v_set:
            for e in a_tuple:
                if isinstance(e, Code):
                    return True

    return False


def test_implementation(test_class, solution):
    """
    :param test_class: the unittest instance
    :param solution: solution obj.
    :return: passes or not
    """

    inputs = get_function_inputs(solution.function)
    tables = solution.processed_conditions.tables
    default_set = set(get_inputs_with_default_output(inputs, tables))
    tables[solution.processed_conditions.default] = default_set

    if has_code_args(tables):
        warnings.warn("Cannot test function, it has added code", UserWarning)
    else:
        for expected_value, tuple_set in tables.iteritems():
            for a_tuple in tuple_set:
                run_single_test(test_class=test_class,
                                a_tuple=a_tuple,
                                solution=solution,
                                expected_value=expected_value)
