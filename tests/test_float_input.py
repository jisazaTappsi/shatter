#!/usr/bin/env python

"""Tests for float_input.py"""

import unittest
from shatter.solver import Rules
from tests.generated_code import float_input_functions as f
from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


class ConstantsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_simple_integer_input(self):
        """
        Simple integer input
        """

        function = f.simple

        code = ["def {}(a):".format(function.__name__),
                "    return a>=2.5"]

        r = Rules()
        r.add(a=0, output=0)
        r.add(a=1, output=0)
        r.add(a=2, output=0)
        r.add(a=3, output=1)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code)

    def test_simple2_integer_input(self):
        """
        Bit more complex Simple integer input
        """

        function = f.bit_more_complex

        code = ["def {}(a):".format(function.__name__),
                "    return (a>=0.5 and a<=2.5)"]

        r = Rules()
        r.add(a=0, output=0)
        r.add(a=1, output=1)
        r.add(a=2, output=1)
        r.add(a=3, output=0)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code)

    def test_2_integer_inputs_easy(self):
        """
        The hypothesis should simplify to single interval of one of the 2 variables.
        """

        function = f.two_inputs_bit_more_complex

        code_solution_1 = ["def {}(a, b):".format(function.__name__),
                           "    return (b>=0.5 and b<=2.5)"]

        code_solution_2 = ["def {}(a, b):".format(function.__name__),
                           "    return (a>=0.5 and a<=2.5)"]

        r = Rules()
        r.add(a=0, b=0, output=0)
        r.add(a=1, b=1, output=1)
        r.add(a=2, b=2, output=1)
        r.add(a=3, b=3, output=0)

        solution = r.solve(function)

        try:
            self.assertEqual(solution.implementation, code_solution_1)
        except AssertionError:
            self.assertEqual(solution.implementation, code_solution_2)

    def test_2_integer_inputs(self):
        """
        The hypothesis that solves this problem is a perfect square on the plane with coordinates (a, b)
        """

        function = f.two_inputs_bit_more_complex

        code = ["def {}(a, b):".format(function.__name__),
                "    return (a>=1.0 and a<=2.0) and (b>=1.0 and b<=2.0)"]

        r = Rules()
        r.add(a=0, b=0, output=0)
        r.add(a=1, b=0, output=0)
        r.add(a=0, b=1, output=0)
        #r.add(a=0, b=1, output=1)
        r.add(a=1, b=1, output=1)
        r.add(a=2, b=2, output=1)
        r.add(a=3, b=2, output=0)
        r.add(a=2, b=3, output=0)
        r.add(a=3, b=3, output=0)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code)

    def test_2_integer_inputs_variant(self):
        """
        Variant of the test above. It is no longer a square.
        """

        function = f.two_inputs_bit_more_complex

        code = ["def {}(a, b):".format(function.__name__),
                "    return (b>=1.0 and b<=2.0) and ((a>=1.5 and a<=2.0) or a<=0.0)"]

        r = Rules()
        r.add(a=0, b=0, output=0)
        r.add(a=1, b=0, output=0)
        r.add(a=0, b=1, output=1)
        r.add(a=1, b=1, output=0)
        r.add(a=2, b=2, output=1)
        r.add(a=3, b=2, output=0)
        r.add(a=2, b=3, output=0)
        r.add(a=3, b=3, output=0)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code)

    def test_2_integer_inputs_bit_more_complex(self):
        """
        Here the QM simplification is tested. There are 2 right solutions.
        """

        function = f.two_inputs_bit_more_complex

        code_solution_1 = ["def {}(a, b):".format(function.__name__),
                           "    return (b>=2.5 and b<=5.5) or a<=1.5"]

        code_solution_2 = ["def {}(a, b):".format(function.__name__),
                           "    return (b>=2.5 and b<=5.5) or b<=1.5"]

        r = Rules()
        r.add(a=4, b=6, output=0)
        r.add(a=5, b=5, output=1)
        r.add(a=6, b=4, output=1)
        r.add(a=3, b=3, output=1)
        r.add(a=2, b=2, output=0)
        r.add(a=1, b=1, output=1)

        solution = r.solve(function)

        # Tries 2 valid solutions.
        try:
            self.assertEqual(solution.implementation, code_solution_1)
        except AssertionError:
            self.assertEqual(solution.implementation, code_solution_2)


if __name__ == '__main__':
    unittest.main()
