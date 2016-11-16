#!/usr/bin/env python

"""Test for solver.py"""

import unittest

from tests.generated_code import tester_functions as f
from tests.testing_helpers import common_testing_code
from mastermind.rules import Rules
from mastermind import tester
from mastermind.solution import Solution

__author__ = 'juan pablo isaza'


class TesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_collision(self):
        """
        The internal test should fail, because the rules have no internal consistency, they are bull...
        """
        cond = Rules(a=True, output=1)  # first condition
        cond.add(a=False, output=1)  # contradictory condition.

        with self.assertRaises(AssertionError):
            cond.solve(f.collision, self)

    def test_non_collision(self):
        """
        Testing bigger stuff. Multiple ifs with multiple boolean variables
        """
        cond = Rules(a=True, b=True, c=True, output=0)  # leave d out
        cond.add(a=False, b=True, d=True, output=1)  # leave c out
        cond.add(a=True, c=False, d=True, output=2)  # leave b out
        cond.add(b=True, c=False, d=False, output=3)  # leave a out

        cond.solve(f.non_collision, self)

    def test_unittest_validation(self):
        """
        Should raise exception if unittest is not of the correct class.
        """
        with self.assertRaises(TypeError):
            tester.test_implementation('wrong class', Solution(None, None, None))

    def test_no_unittests_performed(self):
        """
        Should not perform tests if unittest=None.
        """
        self.assertFalse(tester.test_implementation(None, Solution(None, None, None)))

    def test_function_solve_with_no_unittest(self):
        """
        Same as test_basic_if() test but with no unittest provided.
        """

        function = f.basic_if
        ouput = 'le'
        code = ['def {}(a, b):'.format(function.__name__),
                '',
                '    if b:',
                "        return \"{}\"".format(ouput),
                '',
                '    return False']

        cond = Rules(a=True,
                     b=True,
                     output=ouput)
        cond.add(b=True, output=ouput)

        solution = cond.solve(function)
        self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
