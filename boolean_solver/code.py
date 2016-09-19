#!/usr/bin/env python

"""A class that defines a code, with a string."""

from boolean_solver.custom_operator import CustomOperator

__author__ = 'juan pablo isaza'


class Code:

    def __init__(self, rho=None, lho=None, super_method=None, code_str=None):
        self.rho = rho
        self.lho = lho

        if super_method is not None:
            self.operator = CustomOperator(super_method)
        else:
            self.operator = None

        self.the_locals = {}
        self.code_str = code_str

    # explicit hash definition when overriding __eq__, otherwise hash = None.
    __hash__ = object.__hash__

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code_str == other.code_str

    def __str__(self):
        return self.code_str
