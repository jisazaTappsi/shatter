#!/usr/bin/env python

"""Test for util/last_update_set.py"""

import unittest

from boolean_solver.util.last_update_set import LastUpdateSet

__author__ = 'juan pablo isaza'


class LastUpdateSetTest(unittest.TestCase):

    def test_order(self):

        """Check that order is preserved."""

        s = LastUpdateSet()

        old_list = ['4', '3', '2', '1', '5']

        for e in old_list:
            s.add(e)

        new_list = []
        for e in s:
            new_list.append(e)

        self.assertEqual(new_list, old_list)
