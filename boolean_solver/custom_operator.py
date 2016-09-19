#!/usr/bin/env python

"""A class that defines a custom operator between 2 variables"""


__author__ = 'juan pablo isaza'


class CustomOperator:

    COMPARISON_OPERATORS = {'__eq__': '==',
                            '__ne__': '!=',
                            '__lt__': '<',
                            '__gt__': '>',
                            '__le__': '<=',
                            '__ge__': '>='}

    ARITHMETIC_OPERATORS = {'addition': '+',
                            'subtraction': '-',
                            'multiplication': '*',
                            'division': '/',
                            'modulus': '%',
                            'exponent': '**',
                            'floor_division': '//'}

    LOGICAL_OPERATORS = {'intersection': 'and',
                         'union': 'or',
                         'negation': 'not'}

    def __init__(self, method):
        self.method = method
        if method is not None:
            self.symbol = self.COMPARISON_OPERATORS[self.method.__name__]
        else:
            self.symbol = None
