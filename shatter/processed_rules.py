#!/usr/bin/env python

"""Contains data after processing is done."""

from shatter.rules import *
from shatter.constants import *
from shatter.frozen_dict import FrozenDict
from shatter.code import Code

__author__ = 'juan pablo isaza'


class ProcessedRules:
    """
    Contains the default value of the output and tables. Tables is a dict() containing keys which are the output and
    values that are sets of rows. This sets of rows represent tables. So we have a collection of tables each one with
    its output as keys.
    General form:
    >>>ProcessedRules().tables
    is of the form:
    >>>output1 = 1; output2 = 2
    >>>{output1:{(True, Code('1==3')), (False, False)}, output2:{(...), (...), (...) ...}}
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
