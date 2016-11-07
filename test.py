#!/usr/bin/env python

"""setup the python package.py"""

import unittest
from boolean_solver.solver import Conditions, Code, Output
import start

__author__ = 'juan pablo isaza'


class MyTest(unittest.TestCase):

    """
    1. Set conditions of your boolean function (for True outputs)
    2. Run execute(self, callable, table) where callable is the boolean function
     with the decorator=@solve().
     See examples below:
    """
    def test_AND_function(self):

        # The output is explicitly set to true
        cond = Conditions(a=True, b=True, output=True)
        cond.solve(self, start.and_function)

    def test_ifs(self):
        """
        Testing ifs.
        """
        cond = Conditions(a=False, b=True, output=1)  # non-boolean output
        cond.add(a=True, b=False, output=0)  # non-boolean output
        cond.solve(self, start.if_function)

    def test_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        """
        args = {'a': Code(code_str='not a')}
        out = Output(start.recursive, args)

        cond = Conditions(a=False, output=0, default=out)
        cond.solve(self, start.recursive)

    def test_internal_code(self):
        """
        Testing internal pieces of code
        """
        cond = Conditions(any_non_input_name=Code(code_str='isinstance(a, str)'), output=2)
        cond.solve(self, start.internal_code)
