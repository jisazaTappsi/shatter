#!/usr/bin/env python

"""Functions for test_code_generator.py"""

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
def non_boolean_and(a, b):
    pass


@s.solve()
def mix_true_values(a, b):
    pass


@s.solve()
def mix_false_values(a, b):
    pass


@s.solve()
def ordered_expression(a, b):
    pass


@s.solve()
def fun2(a, b):
    pass


@s.solve()
def fun3(a, b):
    pass


@s.solve()
def fun4(a, b):
    pass


@s.solve()
def fun5(a, b):
    pass


@s.solve()
def fun6(a, b):
    pass


@s.solve()
def fun7(a, b):
    pass


@s.solve()
def fun8(a, b):
    pass


@s.solve()
def fun9(a, b):
    pass


@s.solve()
def output_function_obj(a, b):
    pass


@s.solve()
def mix_output(a, b):
    pass


def no_args():
    pass


@s.solve()
def another_call(a, b):
    pass


@s.solve()
def another_call2(a, b):
    pass


@s.solve()
def recursive(a):
    pass


@s.solve()
def with_string_args():
    pass


@s.solve()
def with_default_value(a, b):
    pass


@s.solve()
def f(a):
    pass


@s.solve()
def g(a):
    pass


@s.solve()
def nested_call(a):
    pass


@s.solve()
def with_internal_code_arg(a):
    pass


@s.solve()
def right_expression_order(array):
    pass


@s.solve()
def factor_pieces_of_code():
    pass

