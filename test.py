#!/usr/bin/env python

"""setup the python package.py"""

import unittest
from boolean_solver import solver
import start

__author__ = 'juan pablo isaza'


import unittest
from boolean_solver import solver
import start


class MyTest(unittest.TestCase):

    """
    1. Set conditions of your boolean function (for True outputs)
    2. Run solver.execute(self, callable, table) where callable is the boolean function
     with the decorator=@solve().
     See examples below:
    """
    def test_AND_function(self):

        # The output is explicitly set to true
        cond = solver.Conditions(a=True, b=True, output=True)
        solver.execute(self, start.and_function, cond)

    def test_ifs(self):
        """
        Testing ifs.
        """
        cond = solver.Conditions(a=False, b=True, output=1)  # non-boolean output
        cond.add(a=True, b=False, output=0)  # non-boolean output
        solver.execute(self, start.if_function, cond)

    def test_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        """
        args = {'a': solver.Code('not a')}
        out = solver.Output(start.recursive, args)

        cond = solver.Conditions(a=False, output=0, default=out)
        solver.execute(self, start.recursive, cond)

    def test_internal_code(self):
        """
        Testing internal pieces of code
        """
        cond = solver.Conditions(any_non_input_name=solver.Code('isinstance(a, str)'), output=2)
        solver.execute(self, start.internal_code, cond)