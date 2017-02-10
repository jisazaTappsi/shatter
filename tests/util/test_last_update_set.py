#!/usr/bin/env python

"""Test for util/last_update_set.py"""

import unittest

from shatter.util.last_update_set import LastUpdateSet

__author__ = 'juan pablo isaza'


class LastUpdateSetTest(unittest.TestCase):

    def test_order(self):

        """Check that order is preserved."""

        s = LastUpdateSet()

        old_list = ['4', '3', '2', '1', '5']

        for e in old_list:
            s.add(e)

        new_list = [e for e in s]

        self.assertEqual(new_list, old_list)


if __name__ == '__main__':
    unittest.main()
