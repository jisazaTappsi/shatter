#!/usr/bin/env python

"""A class that defines a code, with a string."""


__author__ = 'juan pablo isaza'


class Code:

    def __init__(self, code_as_str):
        self.code_as_str = code_as_str

    # explicit hash definition when overriding __eq__, otherwise hash = None.
    __hash__ = object.__hash__

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code_as_str == other.code_as_str
