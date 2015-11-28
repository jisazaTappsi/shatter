__author__ = 'juan pablo isaza'

import unittest

from boolean_solver import solver as s


class MyTest(unittest.TestCase):

    def mc_algorithm_and_translate(self, var_names, mc_input, expected_mc_output, expected_exp):
        """
        Heart of the program. inside goes bits, gets boolean python expression.
        :param var_names: bit variables, eg: [b0, b1].
        :param mc_input: rows of truth table with True as output. eg:{'11'} for and.
        :param expected_mc_output: minimal expression given by Quine McCluskey algorithm.
        :param expected_exp: the expected expression in python.
        :return:pass or not pass.
        """
        mc_set = s.execute_mc_algorithm(mc_input)
        self.assertSetEqual(mc_set, expected_mc_output)

        exp = s.translate_to_python_expression(var_names, mc_set)
        self.assertEqual(exp, expected_exp)

    def test_mc_algorithm_and_translate(self):
        """
        Testing for and, or & xor the "process_for_function".
        :return: pass or not pass
        """
        var_names = ['a', 'b']

        #  and. True values specified
        self.mc_algorithm_and_translate(var_names=var_names,
                                        mc_input={'11'},
                                        expected_mc_output={'11'},
                                        expected_exp='a and b')

        #  or. True values specified
        self.mc_algorithm_and_translate(var_names=var_names,
                                        mc_input={'11', '10', '01'},
                                        expected_mc_output={'1-', '-1'},
                                        expected_exp='a or b')

        #  xor only with ands and or. True values specified
        self.mc_algorithm_and_translate(var_names=var_names,
                                        mc_input={'10', '01'},
                                        expected_mc_output={'10', '01'},
                                        expected_exp='a and not b or not a and b')

    def get_function_code(self, signature, exp_expected, table):
        """
        Tests that a right function definition is generated.
        :param signature: of the function eg: sum(a,b).
        :param table: truth table.
        :return: pass or not pass,
        """
        expected_code = ["def " + signature + ":", "    return " + exp_expected]

        inputs = s.get_function_inputs(signature)
        expression = s.get_function_expression(table, inputs)
        code = s.get_function_implementation(expression, 'def ' + signature)

        self.assertListEqual(code, expected_code)

    # Mock functions, to test the s.execute_and_test().

    @s.solve_boolean()
    def and_function(a, b):
        return a and b

    @s.solve_boolean()
    def or_function(a, b):
        return a or b

    @s.solve_boolean()
    def xor_function(a, b):
        return a and not b or not a and b

    @s.solve_boolean()
    def nand_function(a, b):
        return not b or not a

    @s.solve_boolean()
    def and3_function(a, b, c):
        return a and b and c

    #                b1     b0   output
    and_table = {((False, False), False),
                 ((False, True), False),
                 ((True, False), False),
                 ((True, True), True)}

    or_table = {((False, False), False),
                ((False, True), True),
                ((True, False), True),
                ((True, True), True)}

    xor_table = {((False, False), False),
                 ((False, True), True),
                 ((True, False), True),
                 ((True, True), False)}

    nand_truth_table = {((False, False), True),
                        ((False, True), True),
                        ((True, False), True),
                        ((True, True), False)}

    and3_table = {((True, True, True), True)}

    sig_and = "and_function(a, b)"
    exp_and = "a and b"
    sig_or = "or_function(a, b)"
    exp_or = "a or b"
    sig_xor = "xor_function(a, b)"
    exp_xor = "a and not b or not a and b"
    sig_nand = "nand_function(a, b)"
    exp_nand = "not b or not a"
    sig_and3 = "and3_function(a, b, c)"
    exp_and3 = "a and b and c"

    def test_get_function_implementation(self):
        """
        Testing for and, or & xor the "get_function_implementation".
        :return: pass or not pass
        """
        self.get_function_code(self.sig_and, self.exp_and, self.and_table)
        self.get_function_code(self.sig_or, self.exp_or, self.or_table)
        self.get_function_code(self.sig_xor, self.exp_xor, self.xor_table)

    def factor_execute(self, table, a_callable, signature, expression):
        """
        Factoring test.
        """
        solution = s.execute(self, a_callable, table)
        expected_code = ["    def " + signature + ":", "        return " + expression]
        self.assertListEqual(solution.implementation, expected_code)

    def test_execute(self):

        self.factor_execute(self.and_table, self.and_function, self.sig_and, self.exp_and)
        self.factor_execute(self.or_table, self.or_function, self.sig_or, self.exp_or)
        self.factor_execute(self.xor_table, self.xor_function, self.sig_xor, self.exp_xor)
        self.factor_execute(self.nand_truth_table, self.nand_function, self.sig_nand, self.exp_nand)
        self.factor_execute(self.and3_table, self.and3_function, self.sig_and3, self.exp_and3)
