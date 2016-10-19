#!/usr/bin/env python

"""A class that defines a code, with a string."""

from boolean_solver.custom_operator import CustomOperator

__author__ = 'juan pablo isaza'


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

        self.rho = rho
        self.lho = lho

        if super_method is not None:
            self.operator = CustomOperator(super_method)
        else:
            self.operator = None

        self.the_locals = None
        self.code_str = code_str

    # explicit hash definition when overriding __eq__, otherwise hash = None.
    __hash__ = object.__hash__

    def equal_redefined(self, other):
        """code prints its operands and tries a match on them. They need to match their address location.
        :param other: any object to compare can be Code or another stuff
        :return: boolean indicating strict equality"""

        if isinstance(other, Code):
            non_commutative = str(self.rho) == str(other.rho) and str(self.lho) == str(other.lho)
            commutative = str(self.rho) == str(other.lho) and str(self.lho) == str(other.rho)
            return (non_commutative or commutative) and self.operator == other.operator
        else:
            return False

    def __eq__(self, other):
        """Uses cases strategy to differentiate between raw text init and magicVar. Same as in __str__ method."""

        case = self.get_use_case()
        if case == 0:
            return self.equal_redefined(other)
        elif case == 1:
            # for this case, equality is defined only if other is of type Code and their code_str is equal.
            return isinstance(other, Code) and self.code_str == other.code_str
        else:
            raise NotImplemented

    # TODO: odd way to solve composition, missing locals() complexity.
    """
    def __gt__(self, other):
        return Code(self, other, self.__gt__)

    def __mod__(self, other):
        return Code(self, other, self.__mod__)

    def __rmod__(self, other):
        return Code(self, other, self.__rmod__)

    def __mul__(self, other):
        return Code(self, other, self.__mul__)

    def __rmul__(self, other):
        return Code(self, other, self.__rmul__)
    """

    def get_use_case(self):
        """0 for operands, 1 for code as string and 2 for NotImplemented"""
        # TODO: refactor this shit!
        if self.rho is not None and self.operator is not None and self.lho is not None:
            return 0
        elif self.rho is None and self.operator is None and self.lho is None:
            return 1
        else:
            return 2

    def get_operands_str(self, operand):
        """
        prints according to type.
        :param operand: Can be MagicVar or any other stuff, that is operated on.
        :returns string of that operand, ie enhanced str(operand)"""

        if operand is not None and isinstance(operand, MagicVar):
            return operand.get_variable_name(self.the_locals)
        else:
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
            raise NotImplementedError

    def add_locals(self, the_locals):
        self.the_locals = the_locals


# ---------------------------------- Down here is the class MagicVar and related. --------------------------------------

current_id = 1
ADD_LOCALS = 'add_locals'
DECLARE_LOCAL = 'declare_local'


class MagicVarNotFound(Exception):
    """This class is an exception when the magic var variable is not found in locals()."""

    def __init__(self, exception_type):
        if exception_type == ADD_LOCALS:
            super(MagicVarNotFound, self)\
                .__init__("Could not find local variable. Add optional argument 'local_vars=locals()' to"
                          " solver.execute()")
        elif exception_type == DECLARE_LOCAL:
            super(MagicVarNotFound, self)\
                .__init__("Could not find local variable. Make sure that MagicVars are defined locally.")
        else:
            super(MagicVarNotFound, self)\
                .__init__("Unknown specific reason")


class MagicVar:

    def __init__(self):

        # gets the global id and adds 1 to generate a unique identifier for all objects running anywhere.
        global current_id
        self.id = current_id
        current_id += 1

    def __eq__(self, other):
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

    def __div__(self, other):
        return Code(self, other, self.__div__)

    def __rdiv__(self, other):
        return Code(self, other, self.__rdiv__)

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

    def __get_id__(self):
        return self.id

    @staticmethod
    def get_id(var):
        try:
            return var.__get_id__()
        except AttributeError:
            return -1  # negative value guarantees its not going to match to any other MagicVar, as all their ids are +

    def get_variable_name(self, the_locals):
        """
        :param the_locals: a dictionary result of calling locals().
        :returns the name of the variable or raises exception if not found.
        """
        if the_locals is not None:

            names = [k for k, v in list(the_locals.items()) if self.get_id(v) == self.get_id(self)]

            if len(names) > 0:
                return names[0]
            else:
                raise MagicVarNotFound(DECLARE_LOCAL)
        else:
            raise MagicVarNotFound(ADD_LOCALS)

    # TODO: add indexing capabilities
    """
    def __delitem__(self, key):
        self.__delattr__(key)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    """