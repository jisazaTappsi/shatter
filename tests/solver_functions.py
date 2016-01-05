def test_f():
    return False

#!/usr/bin/env python

"""Functions for solver.py tests"""

from boolean_solver import solver as s

__author__ = 'juan pablo isaza'


# Mock functions
@s.solve_boolean()
def and_function(a, b):
    return a and b


@s.solve_boolean()
def or_function(a, b):
    return a or b


@s.solve_boolean()
def xor_function(a, b):
    return a and not b or not a and b


@s.solve_boolean()
def nand_function(a, b):
    return not b or not a


@s.solve_boolean()
def and3_function(a, b, c):
    return a and b and c


def and_missing_decorator(a, b):
    return a and b


@s.solve_boolean()
def any_method(a, b):
    return False


@s.solve_boolean()
def implicit_xor_function(a, b):
    return a and not b or not a and b


@s.solve_boolean()
def mix_xor_function(a, b):
    return a and not b or not a and b

