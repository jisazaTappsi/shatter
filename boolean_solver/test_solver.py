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
        :return: passes or not
        """
        mc_set = s.execute_mc_algorithm(mc_input)
        self.assertSetEqual(mc_set, expected_mc_output)

        exp = s.translate_to_python_expression(var_names, mc_set)
        self.assertEqual(exp, expected_exp)

    def test_mc_algorithm_and_translate(self):
        """
        Testing for and, or & xor the "process_for_function".
        :return: passes or not
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
        :return: passes or not
        """
        expected_code = ["def " + signature + ":", "    return " + exp_expected]

        inputs = s.get_function_inputs(signature)
        expression = s.get_function_expression(table, inputs)
        code = s.get_function_implementation(expression, 'def ' + signature)

        self.assertListEqual(code, expected_code)

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
        :return: passes or not
        """
        self.get_function_code(self.sig_and, self.exp_and, self.and_table)
        self.get_function_code(self.sig_or, self.exp_or, self.or_table)
        self.get_function_code(self.sig_xor, self.exp_xor, self.xor_table)

    def factor_execute(self, table, a_callable, signature, expression):
        """
        Factoring test.
        """
        solution = s.execute(self, a_callable, table)
        expected_code = ["        def " + signature + ":", "            return " + expression]
        self.assertListEqual(solution.implementation, expected_code)

    def test_execute(self):
        """
        Important test: checking that it can solve simple functions.
        :return: passes or not.
        """

        # Mock functions
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

        self.factor_execute(self.and_table, and_function, self.sig_and, self.exp_and)
        self.factor_execute(self.or_table, or_function, self.sig_or, self.exp_or)
        self.factor_execute(self.xor_table, xor_function, self.sig_xor, self.exp_xor)
        self.factor_execute(self.nand_truth_table, nand_function, self.sig_nand, self.exp_nand)
        self.factor_execute(self.and3_table, and3_function, self.sig_and3, self.exp_and3)

    def test_and_missing_decorator(self):
        """
        Should solve it correctly but show a warning, because of the missing decorator.
        :return: passes or not
        """
        def and_missing_decorator(a, b):
            return a and b

        self.factor_execute(self.and_table, and_missing_decorator, 'and_missing_decorator(a, b)', self.exp_and)

    def test_non_callable(self):
        """
        Checks that the function passed is valid.
        :return: passes or not
        """
        @s.solve_boolean()
        def any_method(a, b):
            return False
        
        non_callable = ''
        self.assertEqual(s.execute(self, non_callable, self.and_table).expression, '')

    def test_wrong_table(self):
        """
        Checks that the table is a set and that the rows are all tuples
        :return: passes or not
        """
        @s.solve_boolean()
        def any_method(a, b):
            return False

        # case 1: table not set
        wrong_table = ''
        self.assertEqual(s.execute(self, any_method, wrong_table).expression, '')

        # case 2: at least 1 row not a tuple
        wrong_table = {(), True}
        self.assertEqual(s.execute(self, any_method, wrong_table).expression, '')

        # case 3: more than one explicit output.
        wrong_table = {((True, True), True, True)}
        self.assertEqual(s.execute(self, any_method, wrong_table).expression, '')

    def test_implicit_table_output(self):
        """
        Checks that implicit table outputs work. Instead of table = {((inputs),True), ...}
        it can work with table = {(inputs), ...}. As the output is redundant.
        :return: passes or not.
        """
        # case 1: all rows are implicit
        implicit_output_xor_table = {(True, False), (False, True)}

        @s.solve_boolean()
        def implicit_xor_function(a, b):
            return a and not b or not a and b

        self.factor_execute(table=implicit_output_xor_table,
                            a_callable=implicit_xor_function,
                            signature=implicit_xor_function.__name__ + '(a, b)',
                            expression=self.exp_xor)

        # case 2: some rows are explicit and some implicit.
        mix_output_xor_table = {((True, False), True), (False, True), ((True, True), False)}

        @s.solve_boolean()
        def mix_xor_function(a, b):
            return a and not b or not a and b

        self.factor_execute(table=mix_output_xor_table,
                            a_callable=mix_xor_function,
                            signature=mix_xor_function.__name__ + '(a, b)',
                            expression=self.exp_xor)
