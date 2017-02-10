#!/usr/bin/env python

"""Test for util/helpers.py"""

import unittest

from shatter.util.helpers import get_function_path, read_file, get_function_code, get_function_line_number,\
    is_private_call, retrieve_name
from shatter.code import Code

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

    def test_is_private_call(self):
        """
        Tests that private_call detects that the context of this call is public.
        """
        self.assertFalse(is_private_call())

    def test_variable_name_retrieval(self):
        """
        Should get the outer most name of the variable. although the call is nested.
        """
        def f(k):
            def g(l):
                return retrieve_name(l)
            return g(k)

        j = Code()
        self.assertEqual(f(j), 'j')


if __name__ == '__main__':
    unittest.main()
