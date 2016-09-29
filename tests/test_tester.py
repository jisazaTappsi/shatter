#!/usr/bin/env python

"""Test for solver.py"""

import unittest

from tests.generated_code import tester_functions as f
from tests.testing_helpers import common_testing_code
from boolean_solver.conditions import Conditions
from boolean_solver.solver import execute

__author__ = 'juan pablo isaza'


class TesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_collision(self):
        """
        The internal test should fail, because the conditions have no internal consistency, they are bull...
        """
        cond = Conditions(a=True, output=1)  # first condition
        cond.add(a=False, output=1)  # contradictory condition.

        with self.assertRaises(AssertionError):
            execute(self, f.collision, cond)

    def test_non_collision(self):
        """
        Testing bigger stuff. Multiple ifs with multiple boolean variables
        """
        cond = Conditions(a=True, b=True, c=True, output=0)  # leave d out
        cond.add(a=False, b=True, d=True, output=1)  # leave c out
        cond.add(a=True, c=False, d=True, output=2)  # leave b out
        cond.add(b=True, c=False, d=False, output=3)  # leave a out

        execute(self, f.non_collision, cond)


if __name__ == '__main__':
    unittest.main()
