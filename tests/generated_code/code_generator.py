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

    if a and b:
        return 1

    return False


@s.solve()
def mix_true_values(a, b):

    if a and not b or not a and b:
        return 1

    return False


@s.solve()
def mix_false_values(a, b):

    if not a and b:
        return 0

    return False


@s.solve()
def ordered_expression(a, b):
    return a or b


@s.solve()
def fun2(a, b):

    if not a and b:
        return 2

    if a and not b:
        return 3

    return False


@s.solve()
def fun3(a, b):

    if not a and b:
        return 2.12345

    if a and not b:
        return 3.12345

    return False


@s.solve()
def fun4(a, b):

    if not a and b:
        return 2

    if a and not b:
        return 3

    return False


@s.solve()
def fun5(a, b):

    if not a and b:
        return "3"

    if a and not b:
        return "2"

    return False


@s.solve()
def fun6(a, b):

    if not a and b:
        return 3j

    if a and not b:
        return 2j

    return False


@s.solve()
def fun7(a, b):

    if not a and b:
        return 3, 3

    if a and not b:
        return 2, 2

    return False


@s.solve()
def fun8(a, b):

    if not a and b:
        return 2

    if a and not b:
        return "3"

    return False


@s.solve()
def fun9(a, b):

    if not a and b:
        return 3.12345

    if a and not b:
        return 3, 3

    return False


@s.solve()
def output_function_obj(a, b):

    if not a and b:
        return fun9

    return False


@s.solve()
def mix_output(a, b):

    if not a and b:
        return "a"
    return a and b


def no_args():
    pass


@s.solve()
def another_call(a, b):

    if not a and b:
        return no_args()

    return False


@s.solve()
def another_call2(a, b):

    if not a and b:
        return another_call(a, b)

    return False


@s.solve()
def recursive(a):

    if not a:
        return 0

    return recursive(not a)


@s.solve()
def with_string_args():
    pass


@s.solve()
def with_default_value(a, b):

    if not a and b:
        return 3

    return 5


@s.solve()
def f(a):
    pass


@s.solve()
def g(a):
    pass


@s.solve()
def nested_call(a):

    if not a:
        return f(g(a))

    return False


@s.solve()
def with_internal_code_arg(a):

    if isinstance(a, str):
        return 2

    return False


@s.solve()
def right_expression_order(array):

    if len(array) > 1 and array[0] and isinstance(array[0], int):
        return "right order!!!"

    return False


@s.solve()
def factor_pieces_of_code(array):

    if isinstance(array[0], int) and isinstance(array[1], int) or isinstance(array[2], int):
        return "factoring!!!"

    return False


@s.solve()
def factor_ordered_pieces_of_code(array):

    if isinstance(array[0], int) and isinstance(array[1], int) or isinstance(array[2], int):
        return "factoring!!!"

    return False
