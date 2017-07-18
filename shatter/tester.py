#!/usr/bin/env python

"""Implements the functions to test generated code."""
import traceback
import unittest

from shatter.code import Code
from shatter.util.helpers import *

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
    :param tables: the variable in processed_rules.
    :return: a set with all used tuples.
    """
    return set([item for k, set_v in tables.items() for item in set_v])


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
    :param expected_value: the value that should have the result to pass the test.
    :return: passes, not passes, or cannot be tested by lack of context :(
    """

    function_call_code = get_eval_code(print_inputs_of_tuple(a_tuple), solution.function)

    try:
        exec("\n".join(solution.implementation))
        returned = eval(function_call_code)
    except:
        w_str = "Cannot test function, probably lack of context, exception is: "
        warnings.warn(w_str, UserWarning)
        traceback.print_exc()
    else:
        test_class.assertEqual(returned, expected_value)


def has_code_args(tables):
    """
    Returns True if any argument in the tables is a Code obj.
    :param tables: dict with keys as outputs and sets of tuples as dict values.
    :return: bool
    """
    for k, v_set in tables.items():
        for a_tuple in v_set:
            for e in a_tuple:
                if isinstance(e, Code):
                    return True

    return False


def validate(test_class):
    """
    Makes sure that the class passed can call the assetEqual() method.
    :param test_class: any unittest class, or other object(will raise type error)
    :return: raise error if wrong class found.
    """
    assert_equal = getattr(test_class, "assertEqual", None)
    if not callable(assert_equal):
        raise TypeError("unittest class of type {0}, has not assertEqual defined.".format(type(test_class)))


def problem_has_boolean_output(tables):
    """
    The problem only has True or False outputs.
    :param tables: all truth tables.
    :return: boolean indicating whether the problem is boolean or not.
    """
    return all([isinstance(k, bool) or k in (0, 1) for k in tables.keys()])


class SolvableWithMLImplementation(Exception):
    """Not all cases have been implemented with machine learning. This error type indicates that this case can be
    solved by running a machine learning algorithm."""
    pass


class NotImplementedWithMLYet(Exception):
    """Not all cases have been implemented with machine learning. This error type indicates that this case
    HAS NOT BEEN IMPLEMENTED YET"""
    pass


def test_implementation(test_class, solution):
    """
    :param test_class: the unittest instance
    :param solution: solution obj.
    :return: False if not test done, True if success or raises error if test doesn't pass.
    """
    if test_class is None:

        # assigns a local class to perform tests.
        class MyTest(unittest.TestCase):
            pass

        test_class = MyTest()

    validate(test_class)

    if solution.processed_rules is None:
        return False
    tables = solution.processed_rules.tables

    if has_code_args(tables):
        warnings.warn("Cannot test function, it has added code", UserWarning)
        return False
    else:
        try:
            for expected_value, tuple_set in tables.items():
                for a_tuple in tuple_set:
                    run_single_test(test_class=test_class,
                                    a_tuple=a_tuple,
                                    solution=solution,
                                    expected_value=expected_value)
        except AssertionError:
            # catches exception and re-raises 2 different exceptions depending if the problem is solvable with
            # current machine learning implementation.
            if problem_has_boolean_output(tables):
                raise SolvableWithMLImplementation()

            # TODO: add implementation
            raise NotImplementedWithMLYet()

        return True
