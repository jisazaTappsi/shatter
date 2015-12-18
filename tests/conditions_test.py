__author__ = 'juan pablo isaza'

import unittest
from boolean_solver import conditions as c


class MyTest(unittest.TestCase):

    def test_get_truth_table(self):

        cond = c.Conditions()
        cond.add_condition(a=False, output='3')
        cond.add_condition(a=True)

        self.assertEqual(cond.get_set_with_tuples(['a', 'b']),
                         {(True, False), ((False, False), '3'), ((False, True), '3'), (True, True)})