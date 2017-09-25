#!/usr/bin/env python

"""Contains data after processing is done."""

from shatter.code import Code
from shatter.constants import *
from shatter.rules import *
from shatter.util.frozen_dict import FrozenDict

__author__ = 'juan pablo isaza'


class ProcessedRules:
    """
    Has 2 properties, the 'default' value of the output and the 'tables'.

    Tables is a dict() where each (key, value) pair are a truth table. Tables have:
    Keys = possible function outputs.
    Values = Are the tables represented with lists containing tuples eg:

    >>> [(True, False), (False, True)]

    These tuples are rows of the truth table where the function should return the output value (the key).

    So we have a collection of tables; each one with its own output as key.

    Example:
    >>> ProcessedRules().tables
    is of the form:
    >>> {1: [(True, Code('1==3')), (False, False)], 2: [(False, True), (True, False)]}

    In this case 1 and 2 are the outputs while (True, Code('1==3')), (False, False) are the rows of the truth table
    , ie the cases where 1 should be returned.
    """

    def __init__(self, tables=FrozenDict(), default=False):
        self.tables = tables
        self.default = default


def get_default_output(rules):
    """
    Gets the default value by iterating over all rows until a default word is caught.
    :param rules: a Rules obj.
    :return: the default value or False if None is found or if rules is not a obj.
    """
    if isinstance(rules, Rules) and rules:
        for row in rules:
            if KEYWORDS[DEFAULT] in row:
                return row[KEYWORDS[DEFAULT]]

        return False
    else:
        return False


def get_processed_rules(rules, function_args):
    """
    :param rules:
    :param function_args: args
    :return: processedRules instance
    """
    tables = get_truth_tables(rules, function_args)
    return ProcessedRules(tables, get_default_output(rules))
