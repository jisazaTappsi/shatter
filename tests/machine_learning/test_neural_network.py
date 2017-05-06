#!/usr/bin/env python

"""Test for code.py"""

import unittest

from shatter.machine_learning import neural_network
from tests.generated_code import code_functions as f
from tests.testing_helpers import common_testing_code


__author__ = 'juan pablo isaza'


class NeuralTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common_testing_code.reset_functions_file(f.__file__, hard_reset=True)

    def test_sequence(self):

        self.assertEqual(neural_network.get_layer_sequence(1), [1])
        self.assertEqual(neural_network.get_layer_sequence(2), [2, 1])
        self.assertEqual(neural_network.get_layer_sequence(3), [3, 3, 2, 2, 1])
        self.assertEqual(neural_network.get_layer_sequence(4), [4, 4, 4, 3, 3, 3, 2, 2, 2, 1])


if __name__ == '__main__':
    unittest.main()
