#!/usr/bin/env python

"""Test for rules.py"""

import unittest
from shatter.rules import *
from tests.testing_helpers import constants as cts

__author__ = 'juan pablo isaza'


class RulesTest(unittest.TestCase):

    def test_get_truth_table(self):
        """
        Input data in different ways.
        """

        # case 1: single condition added on constructor
        r = Rules(a=True, b=True)
        self.assertEqual(r.get_truth_tables(['a', 'b']), {True: [(True, True)]})

        # case 2: adding rules on constructor and with add method.
        r = Rules(a=True, b=True)
        r.add(a=True, b=False)
        self.assertEqual(r.get_truth_tables(['a', 'b']), {True: [(True, True), (True, False)]})

        # case 3: adding 2 arguments, one of them with an output.
        r = Rules()
        r.add(a=False, output=3)
        r.add(a=True)

        self.assertEqual(r.get_truth_tables(['a', 'b']),
                         {3: [(False, True), (False, False)], True: [(True, True), (True, False)]})

    # case 0: empty dict.
    def test_empty_dict_max_positional_arg(self):
        self.assertEqual(Rules.gets_start_positional_idx({}), 0)

    # case 1: no positional args.
    def test_no_positional_arg(self):
        self.assertEqual(Rules.gets_start_positional_idx({1: 2, 3: 4}), 0)

    # case 2: some positional args.
    def test_mix_positional_args(self):
        r = Rules.gets_start_positional_idx({1: 2, POSITIONAL_ARGS_RULE + str(0): 4})
        self.assertEqual(r, 1)

    # case 3: all positional args.
    def test_all_positional_args(self):
        r = Rules.gets_start_positional_idx({POSITIONAL_ARGS_RULE + str(0): 6,
                                                  POSITIONAL_ARGS_RULE + str(1): 4})
        self.assertEqual(r, 2)

    def test_get_truth_tables(self):
        """anomaly case: when rules is not a set or a Rules object. It should raise exception."""
        with self.assertRaises(RulesTypeError):
            get_truth_tables(rules=1, function_args=None)

    def test_correct_variables_order(self):
        """Order should be: function args first (from right to left), then args from condition obj from left to right
        and top to bottom"""

        out = -1

        def f(a, b):
            return a + b

        r = Rules(c=1, d=2, output=out)
        r.add(x=3, y=4, output='other_stuff')
        r.add(e=3, f=4, output=out)

        self.assertEqual(r.get_input_keys(helpers.get_function_inputs(f), out),
                         OrderedSet(['a', 'b', 'c', 'd', 'e', 'f']))

    # --------- test validation --------- #

    def test_non_callable(self):
        """
        Checks that the function passed is valid.
        """
        non_callable = ''
        with self.assertRaises(TypeError):
            solve(non_callable, cts.and_table, self)

    # --------- test validation --------- #


if __name__ == '__main__':
    unittest.main()
