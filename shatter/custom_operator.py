#!/usr/bin/env python

"""A class that defines a custom operator between 2 variables"""


__author__ = 'juan pablo isaza'


class CustomOperator:

    OPERATORS = {'__eq__': '==',  # COMPARISON
                '__ne__': '!=',
                '__lt__': '<',
                '__gt__': '>',
                '__le__': '<=',
                '__ge__': '>=',
                '__add__': '+',  # ARITHMETIC
                '__radd__': '+',
                '__sub__': '-',
                '__rsub__': '-',
                '__mul__': '*',
                '__rmul__': '*',
                '__truediv__': '/',
                '__rtruediv__': '/',
                '__mod__': '%',
                '__rmod__': '%',
                '__pow__': '**',
                '__rpow__': '**',
                '__floordiv__': '//',
                '__rfloordiv__': '//',
                 # TODO: NOT READY TO IMPLEMENT THESE. NOT SURE ABOUT CONSEQUENCES!
                #'intersection': 'and',  # LOGICAL
                #'union': 'or',
                #'negation': 'not'
                 }

    def __init__(self, method):
        self.method = method
        if method is not None:
            self.symbol = self.OPERATORS[self.method.__name__]
        else:
            self.symbol = None

    def __eq__(self, other):
        return self.symbol == other.symbol
