#!/usr/bin/env python

"""Functions for solver.py tests"""

from boolean_solver import solver as s

__author__ = 'juan pablo isaza'


# Mock functions
@s.solve()
def and_function(a, b):
    return a and b


@s.solve()
def or_function(a, b):
    return a or b


@s.solve()
def xor_function(a, b):
    return a and not b or not a and b


@s.solve()
def nand_function(a, b):
    return not a or not b


@s.solve()
def and3_function(a, b, c):
    return a and b and c


def and_missing_decorator(a, b):
    return a and b


@s.solve()
def any_method(a, b):
    pass


@s.solve()
def implicit_xor_function(a, b):
    return a and not b or not a and b


@s.solve()
def mix_xor_function(a, b):
    return a and not b or not a and b

