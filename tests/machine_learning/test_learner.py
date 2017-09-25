#!/usr/bin/env python

"""Test non deterministic systems work"""
import copy
import unittest

from shatter.solver import Rules
from tests.generated_code import learner_functions as f
from tests.testing_helpers import common_testing_code
from shatter.tester import NotImplementedWithMLYet

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

    # TODO: discussion:
    # This seems like a NAND so should be not(a and b) = not a or not b but it gives 'False'
    # because of a design principle which assumes that all non stated truth table possibilities are 'False'
    # rather than assuming they are unknown with equal probability of being 'True' or 'False'
    def test_false_and(self):
        """Has the same combination twice with a output=False while having another one with a contradiction """
        function = f.false_and
        code = ['def {}(a, b):'.format(function.__name__),
                '',
                '    return False']

        r = Rules()

        # 2 correct samples.
        r.add(a=True, b=True, output=False)
        r.add(a=True, b=True, output=False)

        # 1 outlier, the model should learn to ignore it.
        r.add(a=True, b=True, output=True)

        solution = r.solve(function)

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

    def test_complex_function2(self):
        """
        Test a 10 input function.
        """
        function = f.complex_2
        code = ['def {}(a, b, c, d, e, f, g, h, i, j):'.format(function.__name__),
                '    return a and b and c and d and e and f and g and h and i and j']

        # Random rules.
        r = Rules()

        kwargs = {'a': True, 'b': True, 'c': True, 'd': True, 'e': True, 'f': True, 'g': True, 'h': True, 'i': True,
                  'j': True}

        true_kwargs = copy.copy(kwargs)
        true_kwargs['output'] = True
        r.add(**true_kwargs)
        r.add(**true_kwargs)

        # 1 outlier, the model should learn to ignore it.
        false_kwargs = copy.copy(kwargs)
        false_kwargs['output'] = False
        r.add(**false_kwargs)

        solution = r.solve(function, self)

        self.assertEqual(solution.implementation, code)

    def test_raise_exception_with_non_boolean_output(self):
        """Replaces True output for number 10, then it has a non boolean output, should raise NotImplementedWithMLYet"""

        function = f.only_boolean
        r = Rules()
        r.add(a=True, output=10)
        r.add(a=True, output=10)
        r.add(b=True, output=False)

        with self.assertRaises(NotImplementedWithMLYet):
            r.solve(function)


if __name__ == '__main__':
    unittest.main()
