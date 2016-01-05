#!/usr/bin/env python

"""Generates pieces of code that are put together by solver.py"""

import warnings
from boolean_solver import util
from constants import *

__author__ = 'juan pablo isaza'


def get_if_code(indent, boolean_exp, output, returning):
    """
    Gets a if implementation.
    :param indent: The indent of the function.
    :param boolean_exp: a boolean expression.
    :param output: The output to return.
    :return: code as a list.
    """
    if returning:
        r = 'return '
    else:
        r = ''

    return ['',
            indent + '    if ' + boolean_exp + ':',
            indent + '        ' + r + str(output)]


def get_code_piece(bool_expression, indent, the_output):

    if isinstance(the_output, bool):
        return [indent + "    return " + bool_expression]
    else:
        # TODO include returning and non returning inputs.
        return get_if_code(indent, bool_expression, the_output, True)


# TODO: generalize to include different positions.
def insert_code_into_implementation(current_implementation, code, the_output):
    """
    Inserts a piece of code(represented by a list) into the implementation.
    :param current_implementation: list
    :param code: list
    :param the_output: the key from the dictionary.
    :return: new code as list
    """

    if util.var_is_true(the_output):
        return current_implementation[:-1] + code + [current_implementation[-1]]
    else:
        return [current_implementation[0]] + code + current_implementation[1:]


def get_function_implementation(current_implementation, bool_expression, definition, the_output):
    """
    Given definition and expression gets the function implementation.
    :param bool_expression: a boolean expression that can be evaluated.
    :param definition:   def function(input1, input2, ...).
    :return: string list with implementation.
    """
    signature = get_signature(definition)
    indent = re.search(INDENT, definition).group()
    if bool_expression and len(bool_expression) > 0:

        new_code = get_code_piece(bool_expression, indent, the_output)
        if current_implementation == INITIAL_IMPLEMENTATION:
            return [indent + "def " + signature + ":"] + new_code
        else:
            return insert_code_into_implementation(current_implementation, new_code, the_output)

    else:
        warnings.warn('Function: ' + signature + ' has no boolean expression; cannot be implemented', UserWarning)
        return current_implementation


def get_signature(definition):
    """
    Gets the signature of a function given the definition ie: from:'    def sum(a, b):  #bla bla bla' to 'sum(a,b)'
    :param definition:
    :return: string signature.
    """
    return re.search(FUNCTION_PATTERN, definition).group()


def translate_to_python_expression(bool_variables, mc_output):
    """
    Converts the algorithm output to friendlier python code.
    :param bool_variables: tuple with the names of the boolean inputs.
    :param mc_output: set containing strings. see "execute_mc_algorithm" for details.
    :return: python boolean expression
    """
    final_bool = ""

    for i, str_bits in enumerate(mc_output):

        factor = ""

        if i > 0:  # when more than one element on list, join by "or"
            final_bool += " or "

        for j, c in enumerate(str_bits):

            if util.string_has_bits_for_and(str_bits, j):
                factor += " and "

            if c == "1":
                factor += bool_variables[j]

            if c == "0":
                factor += "not " + bool_variables[j]

        final_bool += factor

    return final_bool