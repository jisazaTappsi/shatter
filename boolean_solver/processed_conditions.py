#!/usr/bin/env python

"""Contains data after processing is done."""

from boolean_solver.conditions import *
from boolean_solver.constants import *
from boolean_solver.frozen_dict import FrozenDict
from boolean_solver.code import Code

__author__ = 'juan pablo isaza'


class ProcessedConditions:
    """
    Contains the default value of the output and tables. Tables is a dict() containing keys which are the output and
    values that are sets of rows. This sets of rows represent tables. So we have a collection of tables each one with
    its output as keys.
    General form:
    >>>ProcessedConditions().tables
    is of the form:
    >>>output1 = 1; output2 = 2
    >>>{output1:{(True, Code('1==3')), (False, False)}, output2:{(...), (...), (...) ...}}
    """

    def __init__(self, tables=FrozenDict(), default=False):
        self.tables = tables
        self.default = default


def get_default_output(conditions):
    """
    Gets the default value by iterating over all rows until a default word is caught.
    :param conditions: a Conditions obj.
    :return: the default value or False if None is found or if conditions is not a obj.
    """
    if isinstance(conditions, Conditions) and conditions:
        for row in conditions:
            if KEYWORDS[DEFAULT] in row:
                return row[KEYWORDS[DEFAULT]]

        return False
    else:
        return False


def get_processed_conditions(conditions, function_args):
    """
    :param conditions:
    :param function_args: args
    :return: processConditions instance
    """
    tables = get_truth_tables(conditions, function_args)
    return ProcessedConditions(tables, get_default_output(conditions))
