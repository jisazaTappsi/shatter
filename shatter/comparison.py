#!/usr/bin/env python

"""Class of Objects in charged of comparing variables and numbers."""

__author__ = 'juan pablo isaza'


class Comparison:
    """In charged of comparing variables and numbers."""

    def __init__(self, a, b, operator):
        self.a = a  # number 1
        self.b = b  # number 2
        self.operator = operator  # '>=', '<=', '==' or 'and'

        # TODO: reactivate this, but first fix bug when making intervals (check them they suck)
        #self.simplify()

    def __str__(self):
        out = '{} {} {}'.format(self.a, self.operator, self.b)
        if self.is_composite():
            out = '({})'.format(out)
        return out

    def is_composite(self):
        return isinstance(self.a, Comparison) and isinstance(self.b, Comparison) and self.operator == 'and'

    def get_input(self):
        """
        Returns the variable, it's a string
        :return: string
        """
        return self.a.a if self.is_composite() else self.a

    def composite_has_opposing_operators(self):
        """
        Composite Comparison Objects, that have opposing operators (<=, >=)
        :return: Boolean
        """
        return self.a.operator == '>=' and self.b.operator == '<=' or self.a.operator == '<=' and self.b.operator == '>='

    def should_be_removed(self, my_range, percent_cut):
        """
        Calculates whether the current variable is too particular to consider for the percent cut demanded.
        :param my_range: absolute range of the variable
        :param percent_cut: percentage of absolute range below which the variable should be dropped from dataframe.
        :return: Boolean
        """

        if self.is_composite() and self.composite_has_opposing_operators():

            current_percentage = abs(self.a.b - self.b.b) / abs(my_range[0] - my_range[1])
            return current_percentage < percent_cut

        elif self.operator == '==' and percent_cut > 0:  # if equality
            return True

        return False

    def simplify(self):
        """
        It simplifies expressions like: x2 >= 3.25 and x2 <= 3.25   >>>  x2 == 3.25
        Because this statement is just the single number x2 = 3.25
        :return:
        """
        # it simplifies to an equality
        if self.is_composite() and self.a.b == self.b.b:

            self.a = self.a.a
            self.b = self.b.b
            self.operator = '=='
