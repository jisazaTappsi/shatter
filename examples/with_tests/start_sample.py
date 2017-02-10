#!/usr/bin/env python

"""Example of a use case."""

from shatter.solver import *

__author__ = 'juan pablo isaza'


@solve()
def and_function(a, b):
    pass


@solve()
def or_function(a, b):
    pass


@solve()
def xor_function(a, b):
    pass


@solve()
def and_function_3_variables(a, b, c):
    pass

txt_fail = '''Sorry, run: test_smaple.py
first, to solve the riddle :)'''

txt_success = '''You made it, enjoy :)'''

if __name__ == "__main__":
    and_result = and_function(True, True)  # should be: 'True and True = True', after running test1.
    or_result = or_function(True, False)  # should be: 'True or False = True', after running test1.
    xor_result = xor_function(True, False)  # should be: 'True ^ False = True', after running test1.

    if and_function_3_variables(and_result, or_function, xor_result):  # should be True, after running test1.
        print(txt_success)
    else:
        print(txt_fail)
