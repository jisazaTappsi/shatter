#!/usr/bin/env python

"""Example of a use case."""

import unittest

from examples.with_tests import start_sample
from shatter import solver

__author__ = 'juan pablo isaza'


class MyTest(unittest.TestCase):
    """
    1. Set the truth table of your boolean function (at least for rows where output=True)
    2. run solver.execute(self, callable, table) where callable is the boolean function
     with the decorator=@solve() in functions1.
     See examples below:
    """
    def test_AND_function(self):

        # The output is explicitly set to true
        r = solver.Rules(a=True, b=True, output=True)
        r.solve(start_sample.and_function, self)

    def test_OR_function(self):

        # The output is implicitly set to true
        r = solver.Rules(a=False, b=True)
        r.add(a=True, b=False)
        r.add(a=True, b=True)

        r.solve(start_sample.or_function, self)

    def test_XOR_function(self):

        r = solver.Rules(a=False, b=True)
        r.add(a=True, b=False)

        r.solve(start_sample.xor_function, self)

    def test_AND_3_VARIABLES_function(self):

        r = solver.Rules(a=True, b=True, c=True)
        r.solve(start_sample.and_function_3_variables, self)

print("We have solved the riddle, go run start_sample.py, again!!!")
