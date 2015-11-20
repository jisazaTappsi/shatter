__author__ = 'juan pablo isaza'

import unittest
import solver
from scripts import script1
from scripts import script2


class MyTest(unittest.TestCase):

    def test_FROM_SCRIPT1_function(self):

        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script1.script1_function, truth_table)

    def test_FROM_SCRIPT2_function(self):

        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, script2.script2_function, truth_table)

    # HERE THIS FUNCTION WILL BE AN OR.
    def test_SAME_NAME_function(self):

        truth_table = {((False, False), False),
                       ((False, True), True),
                       ((True, False), True),
                       ((True, True), True)}

        solver.execute(self, script2.same_name_as_other_script_function, truth_table)