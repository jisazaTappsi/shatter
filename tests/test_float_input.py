#!/usr/bin/env python

"""Tests for float_input.py"""

import unittest
import pandas as pd
from sklearn import datasets

from shatter.constants import *
from shatter.solver import Rules
from tests.generated_code import float_input_functions as f
from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


class FloatInputTest(unittest.TestCase):

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
                           "    return (a>=0.5 and a<=2.5)"]

        code_solution_2 = ["def {}(a, b):".format(function.__name__),
                           "    return (b>=0.5 and b<=2.5)"]

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

    def test_many_integer_inputs_easy(self):
        """
        The hypothesis should simplify to single interval of one of the 2 variables.
        """

        function = f.many_inputs_bit_more_complex

        code_abstract_solution = ["def {}(a, b, c, d, e, f):".format(function.__name__),
                                  "    return ({var}>=0.5 and {var}<=2.5)"]

        r = Rules()
        r.add(a=0, b=0, c=0, d=0, e=0, f=0, output=0)
        r.add(a=1, b=1, c=1, d=1, e=1, f=1, output=1)
        r.add(a=2, b=2, c=2, d=2, e=2, f=2, output=1)
        r.add(a=3, b=3, c=3, d=3, e=3, f=3, output=0)

        solution = r.solve(function)

        variables = ['a', 'b', 'c', 'd', 'e', 'f', ]

        for var in variables:
            try:
                code = [code_abstract_solution[0], code_abstract_solution[1].format(var=var)]
                self.assertEqual(solution.implementation, code)
                return  # happy ending
            except AssertionError:
                pass  # still nothing

        raise Exception  #

    def test_2_integer_inputs(self):
        """
        The hypothesis that solves this problem is a perfect square on the plane with coordinates (a, b)
        """

        function = f.two_inputs_bit_more_complex

        code = ["def {}(a, b):".format(function.__name__),
                "    return (a>=1.0 and a<=2.0) and (b>=1.0 and b<=2.0)"]

        r = Rules()
        r.add(a=1, b=0, output=0)
        r.add(a=0, b=1, output=0)
        r.add(a=1, b=1, output=1)
        r.add(a=2, b=2, output=1)
        r.add(a=3, b=2, output=0)
        r.add(a=2, b=3, output=0)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code)

    def test_2_integer_inputs_variant(self):
        """
        Variant of the test above. It is no longer a square.
        """

        function = f.two_inputs_bit_more_complex

        code = ["def {}(a, b):".format(function.__name__),
                "    return (b>=1.0 and b<=2.0) and ((a>=1.5 and a<=2.0) or a<=0.5)"]

        r = Rules()
        r.add(a=1, b=0, output=0)
        r.add(a=0, b=1, output=1)
        r.add(a=1, b=1, output=0)
        r.add(a=2, b=2, output=1)
        r.add(a=3, b=2, output=0)
        r.add(a=2, b=3, output=0)

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

    def test_sklearn_iris_data_set(self):
        """
        Should generate a hypothesis for the sklearn iris data-set with low test error.
        """

        iris = datasets.load_iris()

        x = iris.data
        y = iris.target

        data_frame = pd.DataFrame(x, columns=['x1', 'x2', 'x3', 'x4'])

        # Make binary and add to df
        data_frame[KEYWORDS[OUTPUT]] = [int(bool(e)) for e in y]

        # TODO: solve for the other classes: How to admit less than perfect solutions? introduce max_error, or timeout?
        #data_frame[KEYWORDS[OUTPUT]] = [int(abs(e-1)) for e in y]
        #data_frame[KEYWORDS[OUTPUT]] = [int(bool(abs(e-2))) for e in y]

        function = f.solve_iris

        code_solution_1 = ["def {}(x1, x2, x3, x4):".format(function.__name__),
                           "    return x3 >= 2.45"]

        r = Rules(data_frame)

        solution = r.solve(function)

        self.assertEqual(solution.implementation, code_solution_1)


if __name__ == '__main__':
    unittest.main()
