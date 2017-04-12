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
        Test a non deterministic case when input 'a' is True 66% of the time.
        """

        # TODO: change representation and the table inside non_deterministic.py should be the same.
        # TODO: Also, be able to represent 'a=False' as the more natural 'not a'.
        #from shatter.solver import Code
        #a = Code()
        #r = Rules(a)
        #r.add(a=False)
        #r.add(a)
        #r.solve(f.simple)
        return
        """
        r = Rules(a=True, output=True)
        r.add(a=False, output=True)  # this example is an outlier of the last 2 examples: the model should avoid it.
        r.add(a=True, output=True)
        r.add(a=False, output=False)
        r.add(a=False, output=False)
        r.solve(f.simple, self)

        should_be_true = f.simple(True)
        should_be_false = f.simple(False)

        self.assertTrue(should_be_true)
        self.assertFalse(should_be_false)
        """
        # TODO: the neural network can clean data before applying QM again
        #self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
