#!/usr/bin/env python

"""Test for conditions.py"""

import unittest
from boolean_solver.conditions import *

__author__ = 'juan pablo isaza'


class ConditionsTest(unittest.TestCase):

    def test_get_truth_table(self):
        """
        Input data in different ways.
        """

        # case 1: single condition added on constructor
        cond = Conditions(a=True, b=True)
        self.assertEqual(cond.get_truth_tables(['a', 'b']), {True: {(True, True)}})

        # case 2: adding conditions on constructor and with add method.
        cond = Conditions(a=True, b=True)
        cond.add(a=True, b=False)
        self.assertEqual(cond.get_truth_tables(['a', 'b']), {True: {(True, True), (True, False)}})

        # case 3: adding 2 arguments, one of them with an output.
        cond = Conditions()
        cond.add(a=False, output=3)
        cond.add(a=True)

        self.assertEqual(cond.get_truth_tables(['a', 'b']),
                         {True: {(True, False), (True, True)}, 3: {(False, False), (False, True)}})

    # case 0: empty dict.
    def test_empty_dict_max_positional_arg(self):
        self.assertEqual(Conditions.gets_start_positional_idx({}), 0)

    # case 1: no positional args.
    def test_no_positional_arg(self):
        self.assertEqual(Conditions.gets_start_positional_idx({1: 2, 3: 4}), 0)

    # case 2: some positional args.
    def test_mix_positional_args(self):
        r = Conditions.gets_start_positional_idx({1: 2, POSITIONAL_ARGS_RULE + str(0): 4})
        self.assertEqual(r, 1)

    # case 3: all positional args.
    def test_all_positional_args(self):
        r = Conditions.gets_start_positional_idx({POSITIONAL_ARGS_RULE + str(0): 6,
                                                  POSITIONAL_ARGS_RULE + str(1): 4})
        self.assertEqual(r, 2)

