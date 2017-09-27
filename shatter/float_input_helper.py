#!/usr/bin/env python

"""Helps on some specifics of float_input.py"""

from shatter.constants import *
from shatter.comparison import Comparison

__author__ = 'juan pablo isaza'


def get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


def mean(a, b):
    return (a+b)/2


def add_variable(variables, last_variable, input_var, output, last_input, last_output, input_name):
    """
    Adds or append boolean variable
    :param variables: array with boolean variables
    :param last_variable: the previous variable on the outer for iteration.
    :param input_var: input variable
    :param output: output variable
    :param last_input: the previous input variable on the outer for iteration.
    :param last_output: the previous output variable on the outer for iteration.
    :param input_name: string with name of input variable
    :return: variables list
    """

    if not output and last_output:  # from 1 to 0

        if last_variable is None or last_variable.operator == 'and':  # starts new interval
            variables.append(Comparison(input_name, mean(input_var, last_input), '<='))
        else:  # completes interval
            # TODO: Make intervals the Pythonic may, eg: 2.5 < b < 5.5
            comp2 = Comparison(input_name, mean(input_var, last_input), '<=')
            variables[-1] = Comparison(variables[-1], comp2, 'and')

    elif output and not last_output:  # from 0 to 1

        on_first_var = len(variables) == 1

        # or len(variables) > 0
        if last_variable is None or last_variable.operator == 'and' or on_first_var:  # starts new interval
            variables.append(Comparison(input_name, mean(input_var, last_input), '>='))
        else:  # completes interval
            comp2 = Comparison(input_name, mean(input_var, last_input), '>=')
            variables[-1] = Comparison(variables[-1], comp2, 'and')

    return variables


def get_variables(df, an_input):
    """
    Given a DataFrame and an_input it returns the associated conditions as variables.
    :param df: DataFrame
    :param an_input: string with an input.
    :return: list containing strings. Each string is a condition as well as a variable of the QM problem
    """
    variables = []
    last_output = None
    last_input = None
    for idx, row in df.iterrows():

        input_var = row[an_input]
        output = row[KEYWORDS[OUTPUT]]

        last_variable = get(variables, -1, None)

        if last_output is not None:
            variables = add_variable(variables, last_variable, input_var, output, last_input, last_output, an_input)

        last_output = output
        last_input = input_var

    return variables
