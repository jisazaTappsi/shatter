__author__ = 'juan pablo isaza'

from solver import *


@solve_boolean()
def script2_function(a, b):
    return a and b


@solve_boolean()
def same_name_as_other_script_function(a, b):
    return a or b


@solve_boolean()
def test_on_tests1_function(a, b):
    return a and b
