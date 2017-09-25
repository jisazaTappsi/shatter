#!/usr/bin/env python

"""Test for util/last_update_set.py"""

import unittest

from shatter.util.ordered_set import OrderedSet

__author__ = 'juan pablo isaza'


class OrderedSetTest(unittest.TestCase):

    def test_order(self):

        """Check that order is preserved."""

        s = OrderedSet()

        old_list = ['4', '3', '2', '1', '5']

        for e in old_list:
            s.add(e)

        new_list = [e for e in s]

        self.assertEqual(new_list, old_list)


if __name__ == '__main__':
    unittest.main()
