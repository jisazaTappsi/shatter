#!/usr/bin/env python

"""Test for code_generator.py"""
import unittest

from boolean_solver import code_generator as c
from boolean_solver import solver as s
from boolean_solver.util.helpers import get_function_inputs
from tests.generated_code import code_generator as f
from tests.testing_helpers import constants as cts, common_testing_code

__author__ = 'juan pablo isaza'


class GeneratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(common_testing_code.get_source_path(f.__file__))

    def test_code_generation_with_if(self):
        """
        Test with outputs different from boolean.
        """
        cond = s.Conditions(a=True, b=True, output=1)
        solution = s.execute(self, f.non_boolean_and, cond)

        code = ['def ' + f.non_boolean_and.__name__ + '(a, b):',
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
        """
        expected_code = ["def " + signature + ":", "    return " + expression_expected]

        inputs = get_function_inputs(fun)
        expression = s.get_function_expression(table, inputs)
        definition = 'def ' + signature
        code = s.add_code_to_implementation(current_implementation=s.get_initial_implementation(definition),
                                            bool_expression=expression,
                                            definition=definition,
                                            the_output=True)
        self.assertListEqual(code, expected_code)

    def test_get_function_implementation(self):
        """
        Testing for and, or & xor the "get_function_implementation".
        """
        self.get_function_code(cts.sig_and, cts.exp_and, cts.and_table, f.and_function)
        self.get_function_code(cts.sig_or, cts.exp_or, cts.or_table, f.or_function)
        self.get_function_code(cts.sig_xor, cts.exp_xor, cts.xor_table, f.xor_function)

    def test_boolean_and_quasi_boolean_mix_true_values(self):
        """
        Tests whether changing inputs for True and 1 outputs affect the final result.
        BY DEFAULT IF 1 AND TRUE are present will choose 1 as output.
        Test with both a boolean and quasi-boolean output.
        In python True == 1. Therefore output=1 is the same as output=True.
        """
        code = ['def mix_true_values(a, b):',
                '',
                '    if a and not b or not a and b:',
                '        return 1',
                '',
                '    return False']

        cond = s.Conditions(a=True, b=False, output=1)  # non-boolean output
        cond.add(a=False, b=True, output=True)  # boolean condition
        solution = s.execute(self, f.mix_true_values, cond)
        self.assertEqual(solution.implementation, code)

    def test_boolean_and_quasi_boolean_mix_false_values(self):
        """
        Will make an if for the 0 case, while it will ignore the False case.
        """
        code = ['def mix_false_values(a, b):',
                '',
                '    if not a and b:',
                '        return 0',
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=0)  # non-boolean output
        cond.add(a=True, b=False, output=False)  # boolean condition
        solution = s.execute(self, f.mix_false_values, cond)
        self.assertEqual(solution.implementation, code)

        cond = s.Conditions(a=True, b=False, output=False)  # non-boolean output
        cond.add(a=False, b=True, output=0)  # boolean condition
        solution = s.execute(self, f.mix_false_values, cond)
        self.assertEqual(solution.implementation, code)

    def test_conditions_input_order_is_respected(self):
        """
        First input has to be first on the final boolean expression.
        So programmers can use short circuiting to their advantage ;). Very useful when validating data.
        Changing input order will change expression order.
        """
        code = ['def ordered_expression(a, b):',
                '    return a or b']

        cond = s.Conditions(a=True, output=True)  # boolean output
        cond.add(b=True, output=True)  # boolean condition
        solution = s.execute(self, f.ordered_expression, cond)
        self.assertEqual(solution.implementation, code)

        code = ['def ordered_expression(a, b):',
                '    return a or b']

        cond = s.Conditions(b=True, output=True)  # boolean output
        cond.add(a=True, output=True)  # boolean condition
        solution = s.execute(self, f.ordered_expression, cond)
        self.assertEqual(solution.implementation, code)

    def multiple_value_test(self, out1, out2, function):
        """
        Testing multiple output types.
        :param out1: anything
        :param out2: anything
        :param function: object
        """
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.print_object(out1),
                '',
                '    if a and not b:',
                '        return ' + c.print_object(out2),
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out1)  # non-boolean output
        cond.add(a=True, b=False, output=out2)  # non-boolean condition
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_multiple_outputs(self):
        """
        Test for more than 1 if, outputs are longs.
        """
        uniform_pairs = [(2, 3, f.fun2),
                         (2.12345, 3.12345, f.fun3),
                         (2L, 3L, f.fun4),
                         ('3', '2', f.fun5),
                         (3j, 2j, f.fun6),
                         ((3, 3), (2, 2), f.fun7),
                         (2, '3', f.fun8),
                         (3.12345, (3, 3), f.fun9)]
                         # TODO: include lists dictionaries and sets.
                         #([1, 2, 3], {4, 5, 6}, f.fun10)]

        for values in uniform_pairs:
            self.multiple_value_test(*values)

    def test_function_outputs(self):
        """
        When output is a function.
        """
        function = f.output_function_obj
        out1 = f.fun9
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.print_object(out1),
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out1)  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_mix_output_boolean(self):
        """
        When ifs and pure boolean expression mix.
        """
        function = f.mix_output
        out = 'a'
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.print_object(out),
                '    return a and b']

        cond = s.Conditions(a=False, b=True, output=out)  # non-boolean output
        cond.add(a=True, b=True)  # boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_calling_another_function_no_args(self):
        """
        Invoke function with NO arguments.
        """
        function = f.another_call
        out = f.no_args
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
        Invoke function with arguments.
        """
        function = f.another_call2
        args = {'a': s.Code('a'), 'b': s.Code('b')}
        out_f = f.another_call
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + out_f.__name__ + '(a, b)',
                '',
                '    return False']

        cond = s.Conditions(a=False, b=True, output=out_f, output_args=args)  # non-boolean output
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_default_keyword(self):
        """
        default keyword changes the last return from False to determined value.
        """
        function = f.with_default_value
        out = 3
        default = 5
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + str(out),
                '',
                '    return ' + str(default)]

        cond = s.Conditions(a=False, b=True, output=out, default=default)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

        cond = s.Conditions(a=False, b=True, output=out)
        cond.add(default=default)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        """
        function = f.recursive
        args = {'a': s.Code('not a')}
        out = s.Output(f.recursive, args)
        code = ['def ' + function.__name__ + '(a):',
                '',
                '    if not a:',
                '        return 0',
                '',
                '    return ' + function.__name__ + '(not a)']

        cond = s.Conditions(a=False, output=0, default=out)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_calling_nested_functions(self):
        """
        call nested functions.
        """
        function = f.nested_call
        out_obj = s.Output(f.f, {'a': s.Output(f.g, {'a': s.Code('a')})})
        code = ['def ' + function.__name__ + '(a):',
                '',
                '    if not a:',
                '        return ' + f.f.__name__ + '(' + f.g.__name__ + '(a))',
                '',
                '    return False']

        cond = s.Conditions(a=False, output=out_obj)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_internal_code_arguments(self):
        """
        Do logic with pieces of code that evaluate to boolean.
        """
        function = f.with_internal_code_arg
        code = ['def ' + function.__name__ + '(a):',
                '',
                '    if isinstance(a, str):',
                '        return 2',
                '',
                '    return False']

        cond = s.Conditions(any_non_input_name=s.Code('isinstance(a, str)'), output=2)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_right_code_input_order(self):
        """
        For programmer convenience and to be able to use short circuiting.
        Code pieces on expressions will follow the same order as the input order.
        """

        function = f.right_expression_order
        right_str = 'right order!!!'
        code1_str = 'len(array) > 1'
        code2_str = 'array[0]'
        code3_str = 'isinstance(array[0], int)'

        code = ['def ' + function.__name__ + '(array):',
                '',
                '    if ' + code1_str + ' and ' + code2_str + ' and ' + code3_str + ':',
                '        return ' + "\"" + right_str + "\"",
                '',
                '    return False']

        cond = s.Conditions(s.Code(code1_str),
                            s.Code(code2_str),
                            s.Code(code3_str),
                            output=right_str)
        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_factor_unordered_pieces_of_code(self):
        """
        Tests that string output is factored, when inputs are given all at once.
        """
        function = f.factor_pieces_of_code
        right_str = 'factoring!!!'
        code1_str = 'isinstance(array[0], int)'
        code2_str = 'isinstance(array[1], int)'
        code3_str = 'isinstance(array[2], int)'

        code = ['def ' + function.__name__ + '(array):',
                '',
                '    if ' + code1_str + ' and ' + code2_str + ' or ' + code3_str + ':',
                '        return ' + "\"" + right_str + "\"",
                '',
                '    return False']

        cond = s.Conditions(rule1=s.Code(code1_str),
                            rule2=s.Code(code2_str),
                            output=right_str)

        cond.add(rule3=s.Code(code3_str), output=right_str)

        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_factor_ordered_pieces_of_code(self):
        """
        Tests that string output is factored, when inputs are given in more than one addition.
        """
        function = f.factor_ordered_pieces_of_code
        right_str = 'factoring!!!'
        code1_str = 'isinstance(array[0], int)'
        code2_str = 'isinstance(array[1], int)'
        code3_str = 'isinstance(array[2], int)'

        code = ['def ' + function.__name__ + '(array):',
                '',
                '    if ' + code1_str + ' and ' + code2_str + ' or ' + code3_str + ':',
                '        return ' + "\"" + right_str + "\"",
                '',
                '    return False']

        cond = s.Conditions(s.Code(code1_str),
                            s.Code(code2_str),
                            output=right_str)

        cond.add(s.Code(code3_str), output=right_str)

        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)

    def test_factor_code_output(self):
        """
        Tests that code output can be factored.
        """
        function = f.factor_ordered_pieces_of_code
        output_code = '2*2'
        code1_str = 'isinstance(array[0], int)'
        code2_str = 'isinstance(array[1], int)'

        code = ['def ' + function.__name__ + '(array):',
                '',
                '    if ' + code1_str + ' or ' + code2_str + ':',
                '        return ' + output_code,
                '',
                '    return False']

        cond = s.Conditions(s.Code(code1_str), output=s.Code(output_code))
        cond.add(s.Code(code2_str), output=s.Code(output_code))

        solution = s.execute(self, function, cond)
        self.assertEqual(solution.implementation, code)