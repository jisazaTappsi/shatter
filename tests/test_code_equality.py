#!/usr/bin/env python

"""Test for code.py"""

import unittest

from boolean_solver.code import Code, MagicVar, MagicVarNotFound
from tests.generated_code import code_functions as f
from tests.testing_helpers import common_testing_code


__author__ = 'juan pablo isaza'


i = MagicVar()
j = MagicVar()
code1 = i == j
code2 = i == j
code3 = j == i
code4 = i < j


class CodeTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

	def test_equality_commutative_property_Code(self):
		"""Test commutative property on the Code level. Easy busy"""
		self.assertTrue(code1 == code2)
		self.assertTrue(code2 == code1)

	def test_equality_commutative_property_magic_vars(self):
		"""Test commutative property when building the MagicVars. Not so easy."""
		self.assertTrue(code1 == code3)
		self.assertTrue(code3 == code1)

	def test_inequality_different_operator(self):
		"""Always false if there is an operator mismatch"""
		self.assertFalse(code1 == code4)
		self.assertFalse(code4 == code1)


if __name__ == '__main__':
	unittest.main()
