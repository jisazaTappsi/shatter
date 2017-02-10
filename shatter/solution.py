#!/usr/bin/env python

"""Define object that contains the answer."""

import ast


__author__ = 'juan pablo isaza'


class Solution:
    """
    Contains the data describing the solution to the puzzle.
    """
    def __init__(self, function, rules, processed_rules, implementation=[]):
        """
        :param function: a callable.
        :param rules: object of type rules.
        :param processed_rules: object of time processed rules.
        :param implementation:  List containing each line of code.
        :arg ast: abstract syntax tree of Code.
        :return: Solution object.
        """
        self.implementation = implementation
        self.function = function
        self.rules = rules
        self.processed_rules = processed_rules
        self.ast = ast.parse("\n".join(implementation))
