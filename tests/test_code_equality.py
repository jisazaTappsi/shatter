#!/usr/bin/env python

"""Test for code.py"""

import unittest

from boolean_solver.code import MagicVar
from tests.generated_code import code_functions as f
from tests.testing_helpers import common_testing_code


__author__ = 'juan pablo isaza'


i = MagicVar()
j = MagicVar()


class CodeTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

	def test_inequality_different_operator(self):
		"""Always false if there is an operator mismatch"""
		self.assertFalse((i == j) == (i < j))
		self.assertFalse((i < j) == (i == j))

	def test_equality_comparison_operators(self):

		self.assertTrue((i == j) == (i == j))
		self.assertTrue((i != j) == (i != j))
		self.assertTrue((i < j) == (i < j))
		self.assertTrue((i > j) == (i > j))
		self.assertTrue((i <= j) == (i <= j))
		self.assertTrue((i >= j) == (i >= j))

	def test_equality_arithmetic_operators(self):

		self.assertTrue((i + j) == (i + j))
		self.assertTrue((i + j) == (i + j))
		self.assertTrue((i - j) == (i - j))
		self.assertTrue((i * j) == (i * j))
		self.assertTrue((i / j) == (i / j))
		self.assertTrue((i % j) == (i % j))
		self.assertTrue((i ** j) == (i ** j))
		self.assertTrue((i // j) == (i // j))

	def test_no_commutation_comparison_operators(self):

		self.assertFalse((i == j) == (j == i))
		self.assertFalse((i != j) == (j != i))
		self.assertFalse((i < j) == (j < i))
		self.assertFalse((i > j) == (j > i))
		self.assertFalse((i <= j) == (j <= i))
		self.assertFalse((i >= j) == (j >= i))

	def test_no_commutation_arithmetic_operators(self):

		self.assertFalse((i + j) == (j + i))
		self.assertFalse((i - j) == (j - i))
		self.assertFalse((i * j) == (j * i))
		self.assertFalse((i / j) == (j / i))
		self.assertFalse((i % j) == (j % i))
		self.assertFalse((i ** j) == (j ** i))
		self.assertFalse((i // j) == (j // i))

if __name__ == '__main__':
	unittest.main()
