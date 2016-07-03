#!/usr/bin/env python

"""Test for util/inverse_tree_set.py"""

import unittest

from boolean_solver.util.inverse_tree_set import InverseTreeSet

__author__ = 'juan pablo isaza'


class InverseTreeSetTest(unittest.TestCase):

    def test_order(self):

        """Check that order is preserved."""

        s = InverseTreeSet([])

        old_list = ['4', '2', '1', '3']

        for e in old_list:
            s.add(e)

        new_list = []
        for e in s:
            new_list.append(e)

        self.assertEqual(new_list, ['4', '3', '2', '1'])

