__author__ = 'juan pablo isaza'

import unittest
import solver
from scripts import script1
from scripts import script2


class MyTest(unittest.TestCase):

    def test_AND_function(self):

        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script1.and_function, truth_table)

    def test_OR_function(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), True)}

        solver.execute(self, script1.or_function, truth_table)

    def test_NAND_function(self):

        truth_table = {((False, False), True),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), False)}

        solver.execute(self, script1.nand_function, truth_table)

    def test_XOR_function(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), False)}

        solver.execute(self, script1.xor_function, truth_table)

    def test_ANY_function1(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script1.any_function, truth_table)

    def test_ANY_function2(self):

        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), True),
                       ((True, True), False)}

        solver.execute(self, script1.any2_function, truth_table)

    def test_ANY_function3(self):

        truth_table = {((True, False), True)}

        solver.execute(self, script1.any3_function, truth_table)

    def test_AND_function3(self):

        truth_table = {((True, True, True), True)}

        solver.execute(self, script1.any4_function, truth_table)

    def test_ANY_function4(self):

        truth_table = {((False, False, False), False),
                       ((False, False, True), True),
                       ((False, True, False), True),
                       ((True, True, True), False),
                       ((True, False, True), True)}

        solver.execute(self, script1.any5_function, truth_table)

    # HERE THIS FUNCTION WILL BE AN AND.
    def test_SAME_NAME_function(self):

        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script1.same_name_as_other_script_function, truth_table)

    def test_ON_TESTS1_function(self):

        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script2.test_on_tests1_function, truth_table)