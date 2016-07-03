#!/usr/bin/env python

"""Test for util/helpers.py"""

import unittest

from boolean_solver.util.helpers import get_function_path, read_file, get_function_code, get_function_line_number

__author__ = 'juan pablo isaza'


class UtilTest(unittest.TestCase):

    def get_code(self, f):
        path = get_function_path(f)
        file_code = read_file(path)
        return get_function_code(get_function_line_number(f, file_code), read_file(path))

    def test_get_function_code(self):
        """
        Make sure that we can find the right piece of code always.
        """

        def easy(a, b):
            return a and b

        self.assertEqual(self.get_code(easy), ['        def easy(a, b):',
                                               '            return a and b'])

        def medium(a, b):

            return a or b

        self.assertEqual(self.get_code(medium), ['        def medium(a, b):',
                                                 '',
                                                 '            return a or b'])

        def hard(a, b):
  # wtf
            #guag
            a = False

            return a or b

        self.assertEqual(self.get_code(hard), ['        def hard(a, b):',
                                               '  # wtf',
                                               '            #guag',
                                               '            a = False',
                                               '',
                                               '            return a or b'])