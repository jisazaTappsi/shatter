#!/usr/bin/env python

"""Test for code.py"""

import unittest

from shatter.code import Code
from tests.generated_code import code_functions as f
from tests.testing_helpers import common_testing_code
from shatter.custom_operator import CustomOperator

__author__ = 'juan pablo isaza'


class CodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_inequality_different_operator(self):
        """Always false if there is an operator mismatch"""

        i = Code()
        j = Code()

        m = (i == j)
        k = (i < j)
        self.assertFalse(str(m) == str(k))
        self.assertFalse(str(k) == str(m))

    def test_equality(self):

        i = Code()
        j = Code()

        for s in CustomOperator.OPERATORS.values():
            m = (eval('i {} j'.format(s)))
            k = (eval('i {} j'.format(s)))
            self.assertTrue(str(m) == str(k))

    def test_no_commutation(self):

        i = Code()
        j = Code()

        for s in CustomOperator.OPERATORS.values():
            m = (eval('i {} j'.format(s)))
            k = (eval('j {} i'.format(s)))
            self.assertFalse(str(m) == str(k))


if __name__ == '__main__':
    unittest.main()
