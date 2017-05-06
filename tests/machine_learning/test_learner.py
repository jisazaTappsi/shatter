#!/usr/bin/env python

"""Test non deterministic systems work"""
import unittest

from shatter.solver import Rules
from tests.generated_code import learner_functions as f
from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


class LearnerTest(unittest.TestCase):

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
        Test the identity function when the input 'a' has 1 outlier out of 3 samples.
        """

        code = ['def {}(a):'.format(f.identity.__name__),
                '    return a']

        # 2 correct samples.
        r = Rules(a=True, output=True)
        r.add(a=True, output=True)

        # 1 outlier, the model should learn to ignore it.
        r.add(a=True, output=False)
        solution = r.solve(f.identity, self)

        self.assertEqual(solution.implementation, code)

    def test_hard_identity(self):
        """
        Test the identity function when the input 'a' has 4 outliers out of 9 samples.
        """
        function = f.hard_identity
        code = ['def {}(a):'.format(function.__name__),
                '    return a']

        # Correct samples
        r = Rules(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)
        r.add(a=True, output=True)

        # Outliers
        r.add(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)
        r.add(a=True, output=False)

        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_not_identity(self):
        """
        Test the not-identity function when the input 'a' has 4 outliers out of 9 samples.
        """
        function = f.not_identity
        code = ['def {}(a):'.format(function.__name__),
                '    return not a']

        # Correct samples
        r = Rules(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)
        r.add(a=False, output=True)

        # Outliers
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.add(a=False, output=False)

        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_and(self):
        """
        Test the and function when the input has 1 outlier out of 3 samples.
        """
        function = f.and_f
        code = ['def {}(a, b):'.format(function.__name__),
                '    return a and b']

        # 2 correct samples
        r = Rules(a=True, b=True, output=True)
        r.add(a=True, b=True, output=True)

        # 1 outlier, the model should learn to ignore it.
        r.add(a=True, b=True, output=False)
        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_xor(self):
        """
        Test the and function when the input has 1 outlier out of 4 samples.
        """
        function = f.xor_f
        code = ['def {}(a, b):'.format(function.__name__),
                '    return a and not b or not a and b']

        # 3 correct samples.
        r = Rules(a=False, b=True, output=True)

        r.add(a=True, b=False, output=True)
        r.add(a=True, b=False, output=True)

        # 1 outlier, the model should learn to ignore it.
        r.add(a=True, b=False, output=False)
        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_complex_function(self):
        """
        Test a bit more complex function
        """
        function = f.complex
        code = ['def {}(a, b, c, d):'.format(function.__name__),
                '    return a and b and c or d']

        # 3 correct samples.
        r = Rules(a=True, b=True, c=True, output=True)

        r.add(d=True, output=True)
        r.add(d=True, output=True)

        # 1 outlier, the model should learn to ignore it.
        r.add(d=True, output=False)
        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
