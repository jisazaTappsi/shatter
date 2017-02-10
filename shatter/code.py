#!/usr/bin/env python

"""A class that defines a code, with a string."""

from shatter.custom_operator import CustomOperator
from shatter.util import helpers as h

__author__ = 'juan pablo isaza'

EQUATION = 0
CODE_STRING = 1
SINGLE_VARIABLE = 2
NOT_IMPLEMENTED = 3

current_id = 1


class Code:
    """
    Holds all code that the user enters for evaluation. Is a holder for meta-code.
    """

    def __init__(self, rho=None, lho=None, super_method=None, code_str=None):
        """
        Code can either be specified as string with code_str or with the 3 parameters rho, super_method and lho.
        :param rho: right hand operand.
        :param lho: left hand operand.
        :param super_method: When rho == lho then super_method = __eq__.
        :param code_str: alternatively code can be entered as a string.
        """

        # gets the global id and adds 1 to generate a unique identifier for all objects running anywhere.
        global current_id
        self.id = current_id
        current_id += 1

        self.rho = rho
        self.lho = lho

        if super_method is not None:
            self.operator = CustomOperator(super_method)
        else:
            self.operator = None

        self.code_str = code_str

    # explicit hash definition when overriding __eq__, otherwise hash = None.
    __hash__ = object.__hash__

    def equation_case_equals(self, other):
        """code prints its operands and tries a match on them. They need to match their address location.
        :param other: any object to compare can be Code or another stuff
        :return: boolean indicating strict equality"""

        if isinstance(other, Code):
            non_commutative = str(self.rho) == str(other.rho) and str(self.lho) == str(other.lho)
            return non_commutative and self.operator == other.operator
        else:
            return False

    def _equals(self, other):
        """
        Uses cases strategy to differentiate between different init cases. Same as in __str__ method.
        :param other: any other stuff
        :return: boolean
        """
        case = self.get_use_case()
        if case == EQUATION:
            return self.equation_case_equals(other)
        elif case == CODE_STRING:
            # for this case, equality is defined only if other is of type Code and their code_str is equal.
            return isinstance(other, Code) and self.code_str == other.code_str
        elif case == SINGLE_VARIABLE:
            return self.get_id(self) == self.get_id(other)
        elif case == NOT_IMPLEMENTED:
            raise NotImplementedError
        else:
            raise SystemError("unknown value for case")

    def __eq__(self, other):
        """
        If called from a private context(ie  inside this project), will behave according to _equals(self, other),
        otherwise it will return a Code object.
        :param: other
        :return: boolean for private calls, Code object for public calls.
        """
        private_call = h.is_private_call()
        if private_call:  # case: private call.
            return self._equals(other)
        else:  # case: public call.
            return Code(self, other, self.__eq__)

    def __lt__(self, other):
        return Code(self, other, self.__lt__)

    def __gt__(self, other):
        return Code(self, other, self.__gt__)

    def __le__(self, other):
        return Code(self, other, self.__le__)

    def __ge__(self, other):
        return Code(self, other, self.__ge__)

    def __ne__(self, other):
        return Code(self, other, self.__ne__)

    def __add__(self, other):
        return Code(self, other, self.__add__)

    def __radd__(self, other):
        return Code(self, other, self.__radd__)

    def __mul__(self, other):
        return Code(self, other, self.__mul__)

    def __rmul__(self, other):
        return Code(self, other, self.__rmul__)

    def __sub__(self, other):
        return Code(self, other, self.__sub__)

    def __rsub__(self, other):
        return Code(self, other, self.__rsub__)

    def __truediv__(self, other):
        return Code(self, other, self.__truediv__)

    def __rtruediv__(self, other):
        return Code(self, other, self.__rtruediv__)

    def __mod__(self, other):
        return Code(self, other, self.__mod__)

    def __rmod__(self, other):
        return Code(self, other, self.__rmod__)

    def __pow__(self, power, modulo=None):
        return Code(self, power, self.__pow__)

    def __rpow__(self, power, modulo=None):
        return Code(self, power, self.__rpow__)

    def __floordiv__(self, other):
        return Code(self, other, self.__floordiv__)

    def __rfloordiv__(self, other):
        return Code(self, other, self.__rfloordiv__)

    def get_use_case(self):
        """0 for operands, 1 for code as string and 2 for NotImplemented"""
        # TODO: refactor this shit!
        if self.rho is not None and self.operator is not None and self.lho is not None:
            return EQUATION
        elif self.rho is None and self.operator is None and self.lho is None and self.code_str is not None:
            return CODE_STRING
        elif self.rho is None and self.operator is None and self.lho is None and self.code_str is None:
            return SINGLE_VARIABLE
        else:
            return NOT_IMPLEMENTED

    def __get_id__(self):
        return self.id

    @staticmethod
    def get_id(var):
        try:
            return var.__get_id__()
        except AttributeError:
            return -1  # negative value guarantees its not going to match to any other Code instance, as ids are +

    def __str__(self):
        """different behaviours according to get_use_case()"""
        case = self.get_use_case()

        if case == EQUATION:
            return '{rho} {operator} {lho}'.format(rho=self.rho,
                                                   operator=self.operator.symbol,
                                                   lho=self.lho)
        elif case == CODE_STRING:
            return self.code_str
        elif case == SINGLE_VARIABLE:
            return h.retrieve_name(self)
        elif case == NOT_IMPLEMENTED:
            raise NotImplementedError
        else:
            raise SystemError("unknown value for case")

    # TODO: add indexing capabilities
    """
    def __delitem__(self, key):
        self.__delattr__(key)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    """