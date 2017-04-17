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
    def test_simple(self):
        """
        Test the identity function when the input 'a' has 1 outlier out of 5 samples.
        """

        code = ['def {}(a):'.format(f.identity.__name__),
                '    return a']

        # True -> True: 2 samples where the output is True given True input.
        r = Rules(a=True, output=True)
        r.add(a=True, output=True)

        # False -> False: 2 samples where the output is False given the False input.
        r.add(a=False, output=False)
        r.add(a=False, output=False)

        # Outlier of the False -> False samples, the model should learn to ignore it.
        r.add(a=False, output=True)
        solution = r.solve(f.identity, self)

        self.assertTrue(f.identity(True))
        self.assertFalse(f.identity(False))
        self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
