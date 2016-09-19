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

    def get_use_case(self):
        """0 for operands, 1 for code as string and 2 for NotImplemented"""
        if self.rho is not None and self.operator is not None and self.lho is not None and self.code_str is None:
            return 0
        elif self.rho is None and self.operator is None and self.lho is None and self.code_str is not None:
            return 1
        else:
            return 2

    def get_operands_str(self, operand):
        """had to try-except in order to not import MagicVar, because ir would imply a circular reference, as Code is
        imported in MagicVar class.
        :param operand: Can be MagicVar or any other stuff, that is operated on.
        :returns string of that operand, ie enhanced str(operand)"""

        try:
            return operand.get_variable_name(self.the_locals)
        except AttributeError:
            return str(operand)

    def __str__(self):
        """3 possible behaviors: 0 awesome code with MagicVar. 1 standard code as string. 2 raise error"""
        case = self.get_use_case()

        if case == 0:
            return '{rho} {operator} {lho}'.format(rho=self.get_operands_str(self.rho),
                                                   operator=self.operator.symbol,
                                                   lho=self.get_operands_str(self.lho))
        elif case == 1:
            return self.code_str
        else:
            raise NotImplemented
