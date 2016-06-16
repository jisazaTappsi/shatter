#!/usr/bin/env python

"""Functions for test_tester.py"""

from boolean_solver.solver import *

__author__ = 'juan pablo isaza'


@solve()
def collision(a):
    pass


@solve()
def non_collision(a, b, c, d):

    if a and b and c:
        return 0

    if not a and b and d:
        return 1

    if a and not c and d:
        return 2

    if b and not c and not d:
        return 3

    return False
