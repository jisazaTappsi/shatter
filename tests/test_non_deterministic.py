#!/usr/bin/env python

"""Test non deterministic systems work"""
import unittest

from shatter.solver import Rules
from tests.generated_code import non_deterministic_functions as f
from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


class NonDeterministicTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_double_input_will_not_have_effect(self):
        """Even though the input is fed twice the result is the same."""

        solution = ['def {}(a):'.format(f.double_input.__name__),
                    '    return a']

        r = Rules(a=True, output=True)
        r.add(a=True, output=True)
        s = r.solve(f.double_input)
        self.assertEqual(s.implementation, solution)

    # TODO: pass test.
    def test_simplest(self):
        """
        Test a non deterministic case when input 'a' is True 66% of the time.
        """
        r = Rules(a=True, output=True)
        r.add(a=False, output=True)
        r.add(a=True, output=True)
        r.solve(f.simple)

        with_true = f.simple(True)
        with_false = f.simple(False)

        self.assertTrue(with_true)
        self.assertFalse(with_false)

        #self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
