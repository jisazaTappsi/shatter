#!/usr/bin/env python

"""Test for code_generator.py"""

import unittest
from boolean_solver import solver as s
from boolean_solver.util import get_function_inputs
from tests import cts_for_tests as cts
import code_generator_functions as f

__author__ = 'juan pablo isaza'


class GeneratorTest(unittest.TestCase):

    def test_code_generation_with_if(self):
        """
        Test with outputs different from boolean.
        :return: passes or not
        """
        cond = s.Conditions(a=True, b=True, output=1)
        solution = s.execute(self, f.non_boolean_and, cond)

        code = ['def non_boolean_and(a, b):',
                '',
                '    if a and b:',
                '        return 1',
                '',
                '    return False']
        self.assertEqual(solution.implementation, code)

    def get_function_code(self, signature, expression_expected, table, fun):
        """
        Tests that a right function definition is generated.
        :param signature: of the function eg: sum(a,b).
        :param table: truth table.
        :return: passes or not
        """
        expected_code = ["def " + signature + ":", "    return " + expression_expected]

        inputs = get_function_inputs(fun)
        expression = s.get_function_expression(table, inputs)
        code = s.get_function_implementation(current_implementation=[],
                                             bool_expression=expression,
                                             definition='def ' + signature,
                                             the_output=True)
        self.assertListEqual(code, expected_code)

    def test_get_function_implementation(self):
        """
        Testing for and, or & xor the "get_function_implementation".
        :return: passes or not
        """
        self.get_function_code(cts.sig_and, cts.exp_and, cts.and_table, f.and_function)
        self.get_function_code(cts.sig_or, cts.exp_or, cts.or_table, f.or_function)
        self.get_function_code(cts.sig_xor, cts.exp_xor, cts.xor_table, f.xor_function)

    def test_boolean_and_quasi_boolean_mix(self):
        """
        Tests weather changing inputs for True and 1 outputs affect the final result.
        BY DEFAULT IF 1 AND TRUE are present will choose 1 as output.
        Test with both a boolean and quasi-boolean output.
        I python True == 1. Therefore output=1 is the same as output=True.
        :return: passes or not
        """
        code = ['def fun(a, b):',
                '',
                '    if a and not b or not a and b:',
                '        return 1',
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=1)  # non-boolean output
        cond.add(a=True, b=False, output=True)  # boolean condition
        solution = s.execute(self, f.fun, cond)
        self.assertEqual(solution.implementation, code)

        cond = s.Conditions(a=True, b=False, output=True)  # non-boolean output
        cond.add(a=False, b=True, output=1)  # boolean condition
        solution = s.execute(self, f.fun, cond)
        self.assertEqual(solution.implementation, code)

    # TODO: add test for False and 0 value

    def test_multiple_outputs(self):
        """
        Test for more than 1 if.
        :return: passes or not
        """
        code = ['def fun2(a, b):',
                '',
                '    if a and not b:',
                '        return 3',
                '',
                '    if not a and b:',
                '        return 2',
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=2)  # non-boolean output
        cond.add(a=True, b=False, output=3)  # non-boolean condition
        solution = s.execute(self, f.fun2, cond)
        self.assertEqual(solution.implementation, code)

