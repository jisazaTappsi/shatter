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

    def test_identity(self):
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

        self.assertEqual(solution.implementation, code)

    def test_hard_identity(self):
        """
        Test the identity function when the input 'a' has 7 outliers out of 18 samples.
        """
        function = f.hard_identity
        code = ['def {}(a):'.format(function.__name__),
                '    return a']

        # True -> True: samples where the output is True given True input.
        r = Rules(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)

        # False -> False: samples where the output is False given the False input.
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)

        # Outliers of the False -> False samples, the model should learn to ignore these.
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)

        # Outliers of the True -> True samples, the model should learn to ignore these.
        r.add(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)

        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_almost_identity(self):
        """
        Test the not-identity function when the input 'a' has 7 outliers out of 18 samples.
        """
        function = f.not_identity
        code = ['def {}(a):'.format(function.__name__),
                '    return not a']

        # True -> True: samples where the output is True given True input.
        r = Rules(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)

        # False -> True: samples where the output is False given the False input.
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)

        # Outliers of the False -> True samples, the model should learn to ignore these.
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)

        # Outliers of the True -> False samples, the model should learn to ignore these.
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)

        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

if __name__ == '__main__':
    unittest.main()
