#!/usr/bin/env python

"""Test for solver.py"""

import unittest

from boolean_solver import solver as s, conditions as c
from boolean_solver.code_generator import translate_to_python_expression
from boolean_solver.util.last_update_set import LastUpdateSet
from tests.generated_code import solver as f
from tests.testing_helpers import constants as cts

__author__ = 'juan pablo isaza'


class SolverTest(unittest.TestCase):

    def qm_algorithm_and_translate(self, var_names, qm_input, expected_qm_output, expected_exp):
        """
        Heart of the program. inside goes bits, gets boolean python expression.
        :param var_names: bit variables, eg: [b0, b1].
        :param qm_input: rows of truth table with True as output. eg:{'11'} for and.
        :param expected_qm_output: minimal expression given by Quine McCluskey algorithm.
        :param expected_exp: the expected expression in python.
        :return: passes or not
        """
        qm_ordered_set = s.execute_qm_algorithm(qm_input)
        self.assertSetEqual(set(list(qm_ordered_set)), expected_qm_output)

        exp = translate_to_python_expression(var_names, qm_ordered_set)
        self.assertEqual(exp, expected_exp)

    def test_qm_algorithm_and_translate(self):
        """
        Testing for and, or & xor the "process_for_function".
        """
        var_names = ['a', 'b']

        #  and. True values specified
        self.qm_algorithm_and_translate(var_names=var_names,
                                        qm_input={'11'},
                                        expected_qm_output={'11'},
                                        expected_exp='a and b')

        #  or. True values specified
        self.qm_algorithm_and_translate(var_names=var_names,
                                        qm_input={'11', '10', '01'},
                                        expected_qm_output={'1-', '-1'},
                                        expected_exp='a or b')

        #  xor only with ands and or. True values specified
        self.qm_algorithm_and_translate(var_names=var_names,
                                        qm_input={'10', '01'},
                                        expected_qm_output={'10', '01'},
                                        expected_exp='a and not b or not a and b')

    def factor_execute(self, conditions, a_callable, signature, expression):
        """
        Factoring test.
        """
        solution = s.execute(self, a_callable, conditions)
        expected_code = ["def " + signature + ":", "    return " + expression]
        self.assertListEqual(solution.implementation, expected_code)

    def test_execute(self):
        """
        Important test: checking that it can solve simple functions.
        """
        self.factor_execute(cts.and_table, f.and_function, cts.sig_and, cts.exp_and)
        self.factor_execute(cts.or_table, f.or_function, cts.sig_or, cts.exp_or)
        self.factor_execute(cts.xor_table, f.xor_function, cts.sig_xor, cts.exp_xor)
        self.factor_execute(cts.nand_truth_table, f.nand_function, cts.sig_nand, cts.exp_nand)
        self.factor_execute(cts.and3_table, f.and3_function, cts.sig_and3, cts.exp_and3)

    def test_and_missing_decorator(self):
        """
        Should solve it correctly but show a warning, because of the missing decorator.
        """
        self.factor_execute(cts.and_table, f.and_missing_decorator, 'and_missing_decorator(a, b)', cts.exp_and)

    def test_non_callable(self):
        """
        Checks that the function passed is valid.
        """
        non_callable = ''
        self.assertEqual(len(s.execute(self, non_callable, cts.and_table).ast.body), 0)

    def test_wrong_table(self):
        """
        Checks that the table is a set and that the rows are all tuples
        """
        # case 1: table not set
        wrong_table = ''
        self.assertEqual(len(s.execute(self, f.any_method, wrong_table).ast.body), 0)

        # case 2: at least 1 row not a tuple
        wrong_table = {(), True}
        self.assertEqual(len(s.execute(self, f.any_method, wrong_table).ast.body), 0)

        # case 3: more than one explicit output.
        wrong_table = {((True, True), True, True)}
        self.assertEqual(len(s.execute(self, f.any_method, wrong_table).ast.body), 0)

    def test_implicit_table_output(self):
        """
        Checks that implicit table outputs work. Instead of table = {((inputs),True), ...}
        it can work with table = {(inputs), ...}. As the output is redundant.
        """
        # case 1: all rows are implicit
        implicit_output_xor_table = LastUpdateSet([(True, False), (False, True)])

        self.factor_execute(conditions=implicit_output_xor_table,
                            a_callable=f.implicit_xor_function,
                            signature=f.implicit_xor_function.__name__ + '(a, b)',
                            expression=cts.exp_xor)

        # case 2: some rows are explicit and some implicit.
        mix_output_xor_table = LastUpdateSet([((True, False), True), (False, True), ((True, True), False)])

        self.factor_execute(conditions=mix_output_xor_table,
                            a_callable=f.mix_xor_function,
                            signature=f.mix_xor_function.__name__ + '(a, b)',
                            expression=cts.exp_xor)

    def test_conditions_input(self):
        """
        Test for different inputs given as a conditions object.
        """

        # case 1: simple 2 argument and.
        cond = c.Conditions(a=True, b=True)

        self.factor_execute(conditions=cond,
                            a_callable=f.and_function,
                            signature=f.and_function.__name__ + '(a, b)',
                            expression=cts.exp_and)

        # case 2: multiple adds() with mix output: xor.
        cond = c.Conditions(a=True, b=False, output=True)
        cond.add(a=False, b=True)

        self.factor_execute(conditions=cond,
                            a_callable=f.mix_xor_function,
                            signature=f.mix_xor_function.__name__ + '(a, b)',
                            expression=cts.exp_xor)
