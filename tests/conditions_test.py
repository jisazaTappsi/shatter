__author__ = 'juan pablo isaza'

import unittest
from boolean_solver import conditions as c


class MyTest(unittest.TestCase):

    def test_get_truth_table(self):
        """
        Input data in different ways.
        :return: passes or not
        """

        #case 1: single condition added on constructor
        cond = c.Conditions(a=True, b=True)
        self.assertEqual(cond.get_truth_table(['a', 'b']), {(True, True)})

        #case 2: adding conditions on constructor and with add_condition method.
        cond = c.Conditions(a=True, b=True)
        cond.add(a=True, b=False)
        self.assertEqual(cond.get_truth_table(['a', 'b']), {(True, True), (True, False)})

        # case 3: adding 2 arguments, one of them with an output.
        cond = c.Conditions()
        cond.add(a=False, output='3')
        cond.add(a=True)

        self.assertEqual(cond.get_truth_table(['a', 'b']),
                         {(True, False), ((False, False), '3'), ((False, True), '3'), (True, True)})