#!/usr/bin/env python

"""Functions for test_code_generator.py"""

from boolean_solver import solver as s

__author__ = 'juan pablo isaza'


# Mock functions
@s.solve_boolean()
def and_function(a, b):
    pass

@s.solve_boolean()
def or_function(a, b):
    pass


@s.solve_boolean()
def xor_function(a, b):
    pass


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


@s.solve_boolean()
def fun3(a, b):

    if a and not b:
        return 3.12345

    if not a and b:
        return 2.12345

    return False


@s.solve_boolean()
def fun4(a, b):

    if a and not b:
        return 3

    if not a and b:
        return 2

    return False


@s.solve_boolean()
def fun5(a, b):

    if a and not b:
        return "2"

    if not a and b:
        return "3"

    return False


@s.solve_boolean()
def fun6(a, b):

    if a and not b:
        return 2j

    if not a and b:
        return 3j

    return False


@s.solve_boolean()
def fun7(a, b):

    if a and not b:
        return 2, 2

    if not a and b:
        return 3, 3

    return False


@s.solve_boolean()
def fun8(a, b):

    if a and not b:
        return "3"

    if not a and b:
        return 2

    return False


@s.solve_boolean()
def fun9(a, b):

    if a and not b:
        return 3, 3

    if not a and b:
        return 3.12345

    return False


@s.solve_boolean()
def fun10(a, b):
    pass


@s.solve_boolean()
def fun11(a, b):
    pass


@s.solve_boolean()
def fun12(a, b):
    pass


@s.solve_boolean()
def output_function_obj(a, b):

    if not a and b:
        return fun9

    return False


@s.solve_boolean()
def mix_output(a, b):

    if not a and b:
        return "a"
    return a and b


def no_args_function():
    pass


@s.solve_boolean()
def call_another_function(a, b):

    if not a and b:
        return no_args_function()

    return False


@s.solve_boolean()
def call_another_function2(a, b):

    if not a and b:
        return call_another_function(a, b)

    return False


@s.solve_boolean()
def recursive_function(a):

    if not a:
        return recursive_function(not a)

    return False



