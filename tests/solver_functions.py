#!/usr/bin/env python

"""Functions for solver.py tests"""

from boolean_solver import solver as s

__author__ = 'juan pablo isaza'


# Mock functions
@s.solve()
def and_function(a, b):
    pass


@s.solve()
def or_function(a, b):
    pass


@s.solve()
def xor_function(a, b):
    pass


@s.solve()
def nand_function(a, b):
    pass


@s.solve()
def and3_function(a, b, c):
    pass


def and_missing_decorator(a, b):
    pass


@s.solve()
def any_method(a, b):
    pass


@s.solve()
def implicit_xor_function(a, b):
    pass


@s.solve()
def mix_xor_function(a, b):
    pass

