#!/usr/bin/env python

"""Test for code_generator.py"""
import unittest

from shatter import code_generator as c
from shatter import solver as s
from shatter.rules import Rules
from shatter.util.helpers import get_function_inputs
from tests.generated_code import code_generator_functions as f
from tests.testing_helpers import constants as cts, common_testing_code
from shatter.solver import Code
from shatter import QM_helper

__author__ = 'juan pablo isaza'


class GeneratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_get_signature_exception(self):
        """a non valid definition is given, should raise a FunctionNotFound exception."""

        with self.assertRaises(c.FunctionNotFound):
            c.get_signature_from_definition('invalid_function_definition')

    def test_code_generation_with_if(self):
        """
        Test with outputs different from boolean.
        """
        r = Rules(a=True, b=True, output=1)
        solution = r.solve(f.non_boolean_and, self)

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
        expression = QM_helper.get_boolean_expression(table, inputs, 2)
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

        r = Rules(a=True, b=False, output=1)  # non-boolean output
        r.add(a=False, b=True, output=True)  # boolean condition
        solution = r.solve(f.mix_true_values, self)
        self.assertEqual(solution.implementation, code)

    def test_boolean_and_quasi_boolean_mix_false_values(self):
        """
        Will make an if for the 0 case, while it will ignore the False case.
        """
        code = ['def mix_false_values(a, b):',
                '',
                '    if a and not b or not a and b:',
                '        return 0',
                '',
                '    return False']

        r = Rules(a=False, b=True, output=0)  # non-boolean output
        r.add(a=True, b=False, output=False)  # boolean condition
        solution = r.solve(f.mix_false_values, self)
        self.assertEqual(solution.implementation, code)

        r = Rules(a=True, b=False, output=False)  # non-boolean output
        r.add(a=False, b=True, output=0)  # boolean condition
        solution = r.solve(f.mix_false_values, self)
        self.assertEqual(solution.implementation, code)

    def test_rules_input_order_is_respected(self):
        """
        First input has to be first on the final boolean expression.
        So programmers can use short circuiting to their advantage ;). Very useful when validating data.
        Changing input order will change expression order.
        """
        code = ['def ordered_expression(a, b):',
                '    return a or b']

        r = Rules(a=True, output=True)  # boolean output
        r.add(b=True, output=True)  # boolean condition
        solution = r.solve(f.ordered_expression, self)
        self.assertEqual(solution.implementation, code)

        code = ['def ordered_expression(a, b):',
                '    return a or b']

        r = Rules(b=True, output=True)  # boolean output
        r.add(a=True, output=True)  # boolean condition
        solution = r.solve(f.ordered_expression, self)
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

        r = Rules(a=False, b=True, output=out1)  # non-boolean output
        r.add(a=True, b=False, output=out2)  # non-boolean condition
        solution = r.solve(function)
        self.assertEqual(solution.implementation, code)

    def test_multiple_outputs(self):
        """
        Test for more than 1 if, outputs are longs.
        """
        uniform_pairs = [(2, 3, f.fun2),
                         (2.12345, 3.12345, f.fun3),
                         ('3', '2', f.fun4),
                         (3j, 2j, f.fun5),
                         ((3, 3), (2, 2), f.fun6),
                         (2, '3', f.fun7),
                         (3.12345, (3, 3), f.fun8)]
                         # TODO: include lists dictionaries and sets.
                         #([1, 2, 3], {4, 5, 6}, f.fun10)]

        for values in uniform_pairs:
            self.multiple_value_test(*values)

    def test_function_outputs(self):
        """
        When output is a function.
        """
        function = f.output_function_obj
        out1 = f.fun8
        code = ['def ' + function.__name__ + '(a, b):',
                '',
                '    if not a and b:',
                '        return ' + c.print_object(out1),
                '',
                '    return False']

        r = Rules(a=False, b=True, output=out1)  # non-boolean output
        solution = r.solve(function)
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

        r = Rules(a=False, b=True, output=out)  # non-boolean output
        r.add(a=True, b=True)  # boolean output
        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_calling_another_function_no_args(self):
        """
        Invoke function with NO arguments.
        """
        function = f.another_call
        out = f.no_args
        code = ['def {}(a, b):'.format(function.__name__),
                '',
                '    if not a and b:',
                '        return {}()'.format(out.__name__),
                '',
                '    return False']

        r = Rules(a=False, b=True, output=out, output_args={})  # non-boolean output
        solution = r.solve(function)
        self.assertEqual(solution.implementation, code)

    def test_calling_another_function_with_args(self):
        """
        Invoke function with arguments.
        """
        function = f.another_call2
        args = {'a': s.Code(code_str='a'), 'b': s.Code(code_str='b')}
        out_f = f.another_call
        code = ['def {}(a, b):'.format(function.__name__),
                '',
                '    if not a and b:',
                '        return {}(a, b)'.format(out_f.__name__),
                '',
                '    return False']

        r = Rules(a=False, b=True, output=out_f, output_args=args)  # non-boolean output
        solution = r.solve(function)
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

        r = Rules(a=False, b=True, output=out, default=default)
        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

        r = Rules(a=False, b=True, output=out)
        r.add(default=default)
        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        """
        function = f.recursive
        not_a = 'not a'
        args = {'a': s.Code(code_str=not_a)}
        out = s.Output(function, args)
        code = ['def {}(a):'.format(function.__name__),
                '',
                '    if {}:'.format(not_a),
                '        return 0',
                '',
                '    return {0}({1})'.format(function.__name__, not_a)]

        r = Rules(a=False, output=0, default=out)
        solution = r.solve(function)
        self.assertEqual(solution.implementation, code)

    def test_recursive_iteration(self):
        """
        Will do recursive iteration, extremely cool!!!
        """
        function = f.recursive_iteration
        array_len_0 = 'len(array) == 0'
        array_1 = 'array[1:]'
        args = {'array': s.Code(code_str=array_1)}
        out = s.Output(function, args)
        code = ['def {}(array):'.format(function.__name__),
                '',
                '    if {}:'.format(array_len_0),
                '        return 0',
                '',
                '    return {0}({1})'.format(function.__name__, array_1)]

        r = Rules(r1=s.Code(code_str=array_len_0), output=0, default=out)
        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_calling_nested_functions(self):
        """
        call nested functions.
        """
        function = f.nested_call
        out_obj = s.Output(f.f, {'a': s.Output(f.g, {'a': s.Code(code_str='a')})})
        code = ['def ' + function.__name__ + '(a):',
                '',
                '    if not a:',
                '        return ' + f.f.__name__ + '(' + f.g.__name__ + '(a))',
                '',
                '    return False']

        r = Rules(a=False, output=out_obj)
        solution = r.solve(function)
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

        r = Rules(any_non_input_name=s.Code(code_str='isinstance(a, str)'), output=2)
        solution = r.solve(function, self)
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

        r = Rules(r1=s.Code(code_str=code1_str),
                  r2=s.Code(code_str=code2_str),
                  r3=s.Code(code_str=code3_str),
                  output=right_str)
        solution = r.solve(function, self)
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

        r = Rules(rule1=s.Code(code_str=code1_str),
                  rule2=s.Code(code_str=code2_str),
                  output=right_str)

        r.add(rule3=s.Code(code_str=code3_str), output=right_str)

        solution = r.solve(function, self)
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

        r = Rules(r1=s.Code(code_str=code1_str),
                  r2=s.Code(code_str=code2_str),
                  output=right_str)

        r.add(s.Code(code_str=code3_str), output=right_str)

        solution = r.solve(function, self)
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

        r = Rules(r1=s.Code(code_str=code1_str), output=s.Code(code_str=output_code))
        r.add(s.Code(code_str=code2_str), output=s.Code(code_str=output_code))

        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_factor_ordered_pieces_with_redundancy(self):
        """Tests that string output is factored, when inputs are given in more than one addition."""

        function = f.factor_ordered_pieces_with_redundancy
        right_str = 'factoring!!!'
        code0_str = 'isinstance(array[0], int)'
        code1_str = 'isinstance(array[1], int)'

        code = ['def {}(array):'.format(function.__name__),
                '',
                '    if {}:'.format(code1_str),
                "        return \"{}\"".format(right_str),
                '',
                '    return False']

        r = Rules(r1=s.Code(code_str=code0_str),
                  r2=s.Code(code_str=code1_str),
                  output=right_str)

        r.add(s.Code(code_str=code1_str), output=right_str)

        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    # TODO: auxiliary test: remove?
    def test_basic(self):

        function = f.basic
        code = ['def {}(a, b):'.format(function.__name__),
                '    return b']

        r = Rules(a=True,
                  b=True,
                  output=True)
        r.add(b=True, output=True)

        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_basic_if(self):
        """test basic if statement"""

        function = f.basic_if
        ouput = 'le'
        code = ['def {}(a, b):'.format(function.__name__),
                '',
                '    if b:',
                "        return \"{}\"".format(ouput),
                '',
                '    return False']

        r = Rules(a=True,
                  b=True,
                  output=ouput)
        r.add(b=True, output=ouput)

        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_simple_constant_output(self):
        """
        When the result output of the QM algorithm is an empty expression, that means that regardless
        of the input the output is constant.
        """
        function = f.simple_constant_output
        code = ['def {}(a):'.format(function.__name__),
                '    return True']

        r = Rules(a=True, output=True)
        r.add(a=False, output=True)

        solution = r.solve(function, self)
        self.assertEqual(solution.implementation, code)

    def test_inner_inputs_with_different_outputs(self):
        """
        Inner inputs are not function arguments but are for example pieces of code, that act as inputs to the tables.

        Inside function 'return_solution', on module solver.py:
        On each table iteration the all_inputs variable has to be calculated inside the main function of solver.py
        This is because if not this test fails.
        """
        function = f.many_outputs
        input1 = 'isinstance(a, int)'
        input2 = 'isinstance(a, str)'

        r = Rules(r1=Code(code_str=input1), output=1)
        r.add(r1=Code(code_str='isinstance(a, str)'), output=2)

        solution = r.solve(function, self)

        print(solution.implementation)

        # is taking the correct inputs
        self.assertEqual(solution.implementation[2], '    if {}:'.format(input1))
        self.assertEqual(solution.implementation[5], '    if {}:'.format(input2))


if __name__ == '__main__':
    unittest.main()
