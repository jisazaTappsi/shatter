#!/usr/bin/env python

"""Define object that contains the answer."""

import ast


__author__ = 'juan pablo isaza'


class Solution:
    """
    Contains the data describing the solution to the puzzle.
    """
    def __init__(self, function, conditions, processed_conditions, implementation=[]):
        self.implementation = implementation
        self.function = function
        self.conditions = conditions
        self.processed_conditions = processed_conditions
        self.ast = ast.parse("\n".join(implementation))