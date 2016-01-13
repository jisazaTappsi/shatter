#!/usr/bin/env python

"""Test for code_generator.py"""
import unittest

from boolean_solver import solver as s
from boolean_solver.util import get_function_inputs
from tests import constants as cts
import code_generator_functions as f
import functions
from boolean_solver import code_generator as c


__author__ = 'juan pablo isaza'


class GeneratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        functions.reset_functions_file(functions.get_source_path(f.__file__))

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
        code = s.add_code_to_implementation(current_implementation=[],
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

    def multiple_value_test(self, out1, out2, function):
        """
        Testing multiple output types.
        :param out1: anything
        :param out2: anything
        :param function: object
        :return: passes or not
        """
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if a and not b:',
                '        return ' + c.get_output(out2),
                '',
                '    if not a and b:',
                '        return ' + c.get_output(out1),
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out1)  # non-boolean output
        cond.add(a=True, b=False, output=out2)  # non-boolean condition
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_multiple_outputs(self):
        """
        Test for more than 1 if, outputs are longs.
        :return: passes or not
        """
        uniform_pairs = [(2, 3, f.fun2),
                         (2.12345, 3.12345, f.fun3),
                         (2L, 3L, f.fun4),
                         ('3', '2', f.fun5),
                         (3j, 2j, f.fun6),
                         ((3, 3), (2, 2), f.fun7),
                         (2, '3', f.fun8),
                         (3.12345, (3, 3), f.fun9),]
                         # TODO: include lists dictionaries and sets.
                         #([1, 2, 3], {4, 5, 6}, f.fun10)]

        for values in uniform_pairs:
            self.multiple_value_test(*values)

    def test_function_outputs(self):
        """
        When output is a function.
        :return: passes or not
        """
        function = f.output_function_obj
        out1 = f.fun9
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.get_output(out1),
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out1)  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_mix_output_boolean(self):
        """
        When ifs and pure boolean expression mix.
        :return: passes or not
        """
        function = f.mix_output
        out = 'a'
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.get_output(out),
                '    return a and b']

        cond = s.Conditions(a=False, b=True, output=out)  # non-boolean output
        cond.add(a=True, b=True)  # boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_calling_another_function_no_args(self):
        """
        Invoke function with no arguments.
        :return: passes or not
        """
        function = f.call_another_function
        out = f.no_args_function
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + out.__name__ + '()',
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out, output_args={})  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_calling_another_function_with_args(self):
        """
        Invoke function with no arguments.
        :return: passes or not
        """
        # TODO: differentiate between strings and code input.
        function = f.call_another_function2
        args = {'a': 'a', 'b': 'b'}
        out_f = f.call_another_function
        out = s.Output(out_f, args)
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.get_output(out),
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out_f, output_args=args)  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_our_first_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        :return: passes or not
        """
        function = f.recursive_function
        args = {'a': 'not a'}
        out = s.Output(f.recursive_function, args)
        code = ['def ' + function.__name__ + '(a):',
                '',
                '    if not a:',
                '        return ' + c.get_output(out),
                '',
                '    return False'
                ]
        cond = s.Conditions(a=False, output=out, arguments=args)  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)