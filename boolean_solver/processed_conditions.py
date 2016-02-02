#!/usr/bin/env python

"""Contains data after processing is done."""

from boolean_solver.conditions import *
from boolean_solver.constants import *

__author__ = 'juan pablo isaza'


class ProcessedConditions():

    def __init__(self, tables, default):
        self.tables = tables
        self.default = default


def get_default(conditions):
    """
    Gets the default value by iterating over all rows until a default word is caught.
    :param conditions: a Conditions obj.
    :return: the default value or False if None is found or if conditions is not a obj.
    """
    if isinstance(conditions, Conditions) and conditions:
        for row in conditions:
            if DEFAULT_KEYWORD in row:
                return row[DEFAULT_KEYWORD]

        return False
    else:
        return False


def get_processed_conditions(conditions, inputs):
    tables = get_truth_tables(conditions, inputs)
    return ProcessedConditions(tables, get_default(conditions))
