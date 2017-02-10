#!/usr/bin/env python

"""Test non deterministic systems work"""
import unittest

from shatter.solver import Rules
from tests.generated_code import non_deterministic_functions as f
from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


class NonDeterministicTest(unittest.TestCase):
    pass

    #@classmethod
    #def setUpClass(cls):
    #    common_testing_code.reset_functions_file(f.__file__, hard_reset=True)
#
    #def test_code_generation_with_if(self):
    #    """
    #    Test a non deterministic case when a is True 66% of the time.
    #    """
    #    r = Rules(a=True, output=True)
    #    r.add(a=False, output=True)
    #    solution = r.solve(f.simple, self)
#
    #    code = ['def {}(a, b):'.format(f.simple.__name__),
    #            '',
    #            '    if a and b:',
    #            '        return 1',
    #            '',
    #            '    return False']
    #    self.assertEqual(solution.implementation, code)


if __name__ == '__main__':
    unittest.main()
