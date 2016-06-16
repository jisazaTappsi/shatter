#!/usr/bin/env python

"""Test for solver.py"""

import unittest

from tests.generated_code.tester import *

__author__ = 'juan pablo isaza'


class TesterTest(unittest.TestCase):

    def test_collision(self):
        """
        The internal test should fail, because the conditions have no internal consistency, they are bull...
        """
        cond = Conditions(a=True, output=1)  # first condition
        cond.add(a=False, output=1)  # contradictory condition.

        try:
            execute(self, collision, cond)
        except AssertionError:
            return

        # if goes here then fail!
        self.assertTrue(False)

    def test_non_collision(self):
        """
        Testing bigger stuff. Multiple ifs with multiple boolean variables
        """
        cond = Conditions(a=True, b=True, c=True, output=0)  # leave d out
        cond.add(a=False, b=True, d=True, output=1)  # leave c out
        cond.add(a=True, c=False, d=True, output=2)  # leave b out
        cond.add(b=True, c=False, d=False, output=3)  # leave a out

        execute(self, non_collision, cond)
