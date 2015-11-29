__author__ = 'juan pablo isaza'

from solver import *


@solve_boolean()
def and_function(a, b):
    return a and b


@solve_boolean()
def or_function(a, b):
    return a or b


@solve_boolean()
def xor_function(a, b):
    return a and not b or not a and b


@solve_boolean()
def and_function_3_variables(a, b, c):
    return a and b and c

txt_fail = '''Sorry, run:
$ python -m unittest test_sample
first, to solve the riddle :)'''

txt_success = '''You made it, Congrats !!!
Now, see the functions, enjoy :)'''

if __name__ == "__main__":
    and_result = and_function(True, True)  # should be: 'True and True = True', after running test1.
    or_result = or_function(True, False)  # should be: 'True or False = True', after running test1.
    xor_result = xor_function(True, False)  # should be: 'True ^ False = True', after running test1.

    if and_function_3_variables(and_result, or_function, xor_result):  # should be True, after running test1.
        print txt_success
    else:
        print txt_fail
