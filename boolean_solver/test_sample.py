__author__ = 'juan pablo isaza'

import unittest
import solver
import start_sample


class MyTest(unittest.TestCase):
    """
    1. Set the truth table of your boolean function (at least for rows where output=True)
    2. run solver.execute(self, callable, table) where callable is the boolean function
     with the decorator=@solve_boolean() in functions1.
     See examples below:
    """
    def test_AND_function(self):

        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, start_sample.and_function, truth_table)

    def test_OR_function(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), True)}

        solver.execute(self, start_sample.or_function, truth_table)

    def test_XOR_function(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), False)}

        solver.execute(self, start_sample.xor_function, truth_table)

    def test_AND_3_VARIABLES_function(self):

        truth_table = {((True, True, True), True)}

        solver.execute(self, start_sample.and_function_3_variables, truth_table)

print "We have solved the riddle, go run start_sample.py, again!!!"