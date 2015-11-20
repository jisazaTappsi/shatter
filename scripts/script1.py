__author__ = 'juan pablo isaza'

from solver import *


@solve_boolean()
def or_function(a, b):
    return a or b


@solve_boolean()
def and_function(a, b):
    return a and b


@solve_boolean()
def nand_function(a, b):
    return not b or not a


@solve_boolean()
def xor_function(a, b):
    return a and not b or not a and b


@solve_boolean()
def any_function(a, b):
    return b


@solve_boolean()
def any2_function(a, b):
    return a and not b


@solve_boolean()
def any3_function(a, b):
    return a and not b


@solve_boolean()
def any4_function(a, b, c):
    return a and b and c


@solve_boolean()
def any5_function(a, b, c):
    return not a and b and not c or not b and c


@solve_boolean()
def script1_function(a, b):
    return a and b


@solve_boolean()
def same_name_as_other_script_function(a, b):
    return a and b


and_function(False, False)
or_function(True, True)

