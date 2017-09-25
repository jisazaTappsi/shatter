#!/usr/bin/env python

"""
Defines classes and methods to package data for machine learning.
"""
import pandas as pd
from shatter.util.code_dict import CodeDict

__author__ = 'juan pablo isaza'


class LabeledData:
    """
    Suitable for Supervised Machine learning problem.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


def from_lists_to_dict(x, y):
    """
    This is the inverse function of
    >>> def from_dict_to_lists(truth_tables):

    Changes data representation from a machine learning representation (x, y pairs)
    to a truth_tables representation (dict with each output as key and values the truth table.)
    :param x: machine learning inputs.
    :param y: machine learning outputs.
    Table object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: Tables dictionary, contains tables (see ProcessedRules class definition in shatter/processed_rules.py).
    """
    d = CodeDict()
    s = set(y)

    for out in s:
        y_indices = [idx for idx, e in enumerate(y) if e == out]
        x_values = [x[idx] for idx in y_indices]
        d[out] = x_values

    return d


def from_dict_to_lists(truth_tables):
    """
    This is the inverse function of
    >>> def from_lists_to_dict(x, y):

    Changes data representation from a dict to 2 arrays one with inputs and the other one with outputs
    (the x and y in machine learning).
    :param truth_tables: tables with possible contradictions.
    Table object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: A LabeledData object suitable for machine learning.
    """
    x = []
    y = []
    for k, v in truth_tables.items():
        x += v
        y += [k] * len(v)

    return LabeledData(x, y)


def from_dict_to_data_frame(truth_tables, columns):
    """
    Returns a Pandas DataFrame with all the info
    :param truth_tables: dict.
    :param columns: list of all columns
    :return: DataFrame
    """

    data = from_dict_to_lists(truth_tables)

    return pd.DataFrame([tuple(x)+(y,) for x, y in zip(data.x, data.y)], columns=columns)
