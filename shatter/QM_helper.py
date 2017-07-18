#!/usr/bin/env python

"""Defines Quine McCluskey helper methods"""

from shatter import qm
from shatter.rules import Rules
from shatter.util import helpers as h
from shatter.code_generator import translate_to_python_expression

__author__ = 'juan pablo isaza'


def from_table_to_ones(table):
    """
    Gets the ones as a list of strings from a truth table like set, containing tuples.
    :param table: truth table
    :return: list containing bits.
    """
    ones = []
    for row in table:

        # case 1: when the output is explicit.
        if Rules.is_explicit(row):
            if row[1]:  # only do it for true outputs.# TODO change for non booleans.
                ones.append(''.join(list(map(h.from_bool_to_bit, list(row[0])))))

        else:  # case 2: The output is an implicit True, inputs are in the row.
            ones.append(''.join(list(map(h.from_bool_to_bit, list(row)))))

    return ones


def execute_qm_algorithm(ones):
    """
    Quine McCluskey algorithm.
    outputs the minimal boolean expression. Assumes that all none ones have a False output.
    :param ones: input combinations for which output is true
    :return: set containing lists of boolean expressions encoded as strings.
    Where: '1' = boolean ,'0' = not(boolean), '-' = don't care, '^^' = boolean0 ^ boolean1
    Example: set('1-','-0') = bit0 or not bit1
    """
    # TODO: cannot solve ones = ['00'] or a not(or(b0,b1))
    # TODO: change to True, add XOR logic
    qm_obj = qm.QuineMcCluskey(use_xor=False)
    return qm_obj.simplify_los(ones)


def get_boolean_expression(table, inputs, the_output):
    """
    Get boolean expression. Can return empty string.
    solution provided by Quine-McCluskey algorithm.
    outputs a function that maps {0,1} -> {0,1}.
    :param inputs: Function explicit inputs or implicit added rules.
    :param table: truth table.
    :param the_output: function output
    :return: string with boolean expression.
    """
    ones = from_table_to_ones(table)
    if len(ones) > 0:
        qm_output = execute_qm_algorithm(ones)
        expression = translate_to_python_expression(inputs, qm_output)
    else:
        expression = ''

    if expression == '':
        return '{}'.format(the_output)  # This happens when regardless of the input the output is the same
    else:
        return expression
