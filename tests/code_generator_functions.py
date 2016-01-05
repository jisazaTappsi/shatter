#!/usr/bin/env python

"""Functions for test_code_generator.py"""

from boolean_solver import solver as s

__author__ = 'juan pablo isaza'


# Mock functions
@s.solve_boolean()
def and_function(a, b):
    return False


@s.solve_boolean()
def or_function(a, b):
    return False


@s.solve_boolean()
def xor_function(a, b):
    return False


@s.solve_boolean()
def non_boolean_and(a, b):

    if a and b:
        return 1

    return False


@s.solve_boolean()
def fun(a, b):

    if a and not b or not a and b:
        return 1

    return False


@s.solve_boolean()
def fun2(a, b):

    if a and not b:
        return 3

    if not a and b:
        return 2

    return False
