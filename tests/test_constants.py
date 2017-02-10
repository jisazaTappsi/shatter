#!/usr/bin/env python

"""Tests for constants.py, everything here has tests..."""

import unittest
import re

from shatter import constants as cts

__author__ = 'juan pablo isaza'


class ConstantsTest(unittest.TestCase):

    def test_parse_definition(self):
        """
        Parse function.
        """

        # easy one.
        pat = re.search(cts.DEFINITION_PATTERN, 'def fun(a, b):')
        self.assertIsNotNone(pat)

        # medium one
        pat = re.search(cts.DEFINITION_PATTERN, '   def fun(a) :')
        self.assertIsNotNone(pat)

        # hard one
        pat = re.search(cts.DEFINITION_PATTERN, '   def    fun(   a  ,  b   )   :# anything')
        self.assertIsNotNone(pat)

        # even harder
        pat = re.search(cts.DEFINITION_PATTERN, '   def    fun   (   a  ,  b   )   :  # anything # other stuff')
        self.assertIsNotNone(pat)

        # hard solve decorator
        pat = re.search(cts.SOLVE_DECORATOR_PATTERN, '    @ s . solve ()   # anything')
        self.assertIsNotNone(pat)


if __name__ == '__main__':
    unittest.main()
