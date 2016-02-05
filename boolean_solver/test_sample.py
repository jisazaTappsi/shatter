#!/usr/bin/env python

"""Example of a use case."""

import unittest
import solver
import start_sample

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
        cond = solver.Conditions(a=True, b=True, output=True)
        solver.execute(self, start_sample.and_function, cond)

    def test_OR_function(self):

        # The output is implicitly set to true
        cond = solver.Conditions(a=False, b=True)
        cond.add(a=True, b=False)
        cond.add(a=True, b=True)

        solver.execute(self, start_sample.or_function, cond)

    def test_XOR_function(self):

        cond = solver.Conditions(a=False, b=True)
        cond.add(a=True, b=False)

        solver.execute(self, start_sample.xor_function, cond)

    def test_AND_3_VARIABLES_function(self):

        cond = solver.Conditions(a=True, b=True, c=True)
        solver.execute(self, start_sample.and_function_3_variables, cond)

print "We have solved the riddle, go run start_sample.py, again!!!"