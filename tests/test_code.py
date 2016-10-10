#!/usr/bin/env python

"""Test for code.py"""

import unittest

from boolean_solver.code import Code, MagicVar, MagicVarNotFound
from tests.generated_code import code_functions as f
from boolean_solver import solver as s
from tests.testing_helpers import common_testing_code


__author__ = 'juan pablo isaza'


class CodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_comparison_operators(self):

        i = MagicVar()
        j = MagicVar()
        self.assertTrue(isinstance(i == 2, Code))
        self.assertTrue(isinstance(2 == i, Code))
        self.assertTrue(isinstance(i == j, Code))
        self.assertTrue(isinstance(i != 2, Code))
        self.assertTrue(isinstance(2 != i, Code))
        self.assertTrue(isinstance(i != j, Code))
        self.assertTrue(isinstance(i < 2, Code))
        self.assertTrue(isinstance(2 < i, Code))
        self.assertTrue(isinstance(i < j, Code))
        self.assertTrue(isinstance(i > 2, Code))
        self.assertTrue(isinstance(2 > i, Code))
        self.assertTrue(isinstance(i > j, Code))
        self.assertTrue(isinstance(i <= 2, Code))
        self.assertTrue(isinstance(2 <= i, Code))
        self.assertTrue(isinstance(i <= j, Code))
        self.assertTrue(isinstance(i >= 2, Code))
        self.assertTrue(isinstance(2 >= i, Code))
        self.assertTrue(isinstance(i >= j, Code))

    def test_arithmetic_operators(self):

        i = MagicVar()
        j = MagicVar()
        self.assertTrue(isinstance(i + 2, Code))
        self.assertTrue(isinstance(2 + i, Code))
        self.assertTrue(isinstance(i + j, Code))
        self.assertTrue(isinstance(i - 2, Code))
        self.assertTrue(isinstance(2 - i, Code))
        self.assertTrue(isinstance(i - j, Code))
        self.assertTrue(isinstance(i * 2, Code))
        self.assertTrue(isinstance(2 * i, Code))
        self.assertTrue(isinstance(i * j, Code))
        self.assertTrue(isinstance(i / 2, Code))
        self.assertTrue(isinstance(2 / i, Code))
        self.assertTrue(isinstance(i / j, Code))
        self.assertTrue(isinstance(i % 2, Code))
        self.assertTrue(isinstance(2 % i, Code))
        self.assertTrue(isinstance(i % j, Code))
        self.assertTrue(isinstance(i ** 2, Code))
        self.assertTrue(isinstance(2 ** i, Code))
        self.assertTrue(isinstance(i ** j, Code))
        self.assertTrue(isinstance(i // 2, Code))
        self.assertTrue(isinstance(2 // i, Code))
        self.assertTrue(isinstance(i // j, Code))

    # TODO: NOT READY TO IMPLEMENT THESE. NOT SURE ABOUT CONSEQUENCES!
    """
    def test_logical_operators(self):

        i = MagicVar()
        j = MagicVar()
        self.assertTrue(isinstance(i and 2, Code))
        self.assertTrue(isinstance(2 and i, Code))
        self.assertTrue(isinstance(i and j, Code))
        self.assertTrue(isinstance(i or 2, Code))
        self.assertTrue(isinstance(2 or i, Code))
        self.assertTrue(isinstance(i or j, Code))
        self.assertTrue(isinstance(i not 2, Code))
        self.assertTrue(isinstance(2 not i, Code))
        self.assertTrue(isinstance(i not j, Code))
    """

    # TODO: missing the real part of composition!.
    def test_composition(self):

        i = MagicVar()
        j = MagicVar()

        c1 = i == j
        c1.add_locals(locals())
        self.assertEqual(str(c1), 'i == j')

        #c4 = i % j
        #c4.add_locals(locals())

        #c3 = c4 * 2
        #c3.add_locals(locals())

        #c2 = c3 > j
        #c2.add_locals(locals())
        #self.assertEqual(str(c2), 'i * 2 > j')

    def test_magic_with_int(self):
        """
        When user declares
        >>> v = MagicVar()
        and
        >>> code_object = v == 2
        Then code_object should be of type Code, rather than boolean and
        >>>str(code_object)
        'v == 2'
        """

        v = MagicVar()
        code_object = v == 2
        code_object.add_locals(locals())

        self.assertTrue(isinstance(code_object, Code))
        self.assertEqual(str(code_object), 'v == 2')

    def test_magic_with_magic(self):
        """
        When user declares
        >>> v = MagicVar()
        >>> w = MagicVar()
        and
        >>> code_object = v == w
        Then code_object should be of type Code, rather than boolean and
        >>>str(code_object)
        'v == w'
        """

        v = MagicVar()
        w = MagicVar()
        code_object = v == w
        code_object.add_locals(locals())

        self.assertTrue(isinstance(code_object, Code))
        self.assertEqual(str(code_object), 'v == w')

    def test_variable_not_found(self):
        """
        If User forgets to call:
        >>> code_obj = Code()
        >>> code_obj.add_locals(locals())
        it should display:
        >>> MagicVarNotFound("friendly message")
        Exception with friendly message.
        """

        v = MagicVar()
        w = MagicVar()
        code_object = v == w

        self.assertTrue(isinstance(code_object, Code))
        with self.assertRaises(MagicVarNotFound):
            str(code_object)

    def test_factoring_with_magic_var(self):
        """This is a hard test from test_code_generator.py, but additionally here it is added MagicVars :)"""
        function = f.factor_code_with_magic
        output_code = 'i * 2'
        code1_str = 'i == 9'
        code2_str = 'i == 7'

        code = ['def ' + function.__name__ + '(i):',
                '',
                '    if ' + code1_str + ' or ' + code2_str + ':',
                '        return ' + output_code,
                '',
                '    return False']

        i = MagicVar()
        cond = s.Conditions(i == 9, output=i*2)
        cond.add(i == 7, output=i*2)
        solution = s.execute(self, function, cond, local_vars=locals())

        self.assertEqual(solution.implementation, code)

    def test_factor_ordered_with_magic(self):
        """This is a hard test from test_code_generator.py, but additionally here it is added MagicVars :)"""

        function = f.factor_ordered_with_magic
        right_str = 'i * j'
        code1_str = 'i != 0'
        code2_str = 'i < 1'
        code3_str = 'i > j'

        code = ['def ' + function.__name__ + '(i, j):',
                '',
                '    if {0} and {1} or {2}:'.format(code1_str, code2_str, code3_str),
                '        return ' + right_str,
                '',
                '    return False']

        i = MagicVar()
        j = MagicVar()
        cond = s.Conditions(i != 0,
                            i < 1,
                            output=i * j)
        cond.add(i > j, output=i * j)
        solution = s.execute(self, function, cond, local_vars=locals())

        self.assertEqual(solution.implementation, code)

if __name__ == '__main__':
    unittest.main()
