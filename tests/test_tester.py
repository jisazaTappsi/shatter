#!/usr/bin/env python

"""Test for solver.py"""

import unittest

from tests.generated_code import tester_functions as f
from tests.testing_helpers import common_testing_code
from shatter.rules import Rules
from shatter import tester
from shatter.solution import Solution

__author__ = 'juan pablo isaza'


class TesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_collision(self):
        """
        The internal test should fail, because the rules have no internal consistency, they are bull...
        """
        r = Rules(a=True, output=1)  # first condition
        r.add(a=False, output=1)  # contradictory condition.

        with self.assertRaises(AssertionError):
            r.solve(f.collision, self)

    def test_non_collision(self):
        """
        Testing bigger stuff. Multiple ifs with multiple boolean variables
        """
        r = Rules(a=True, b=True, c=True, output=0)  # leave d out
        r.add(a=False, b=True, d=True, output=1)  # leave c out
        r.add(a=True, c=False, d=True, output=2)  # leave b out
        r.add(b=True, c=False, d=False, output=3)  # leave a out

        r.solve(f.non_collision, self)

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

        r = Rules(a=True,
                     b=True,
                     output=ouput)
        r.add(b=True, output=ouput)

        solution = r.solve(function)
        self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
