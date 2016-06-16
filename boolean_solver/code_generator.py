#!/usr/bin/env python

"""Generates pieces of code that are put together by solver.py"""

import warnings

from boolean_solver import conditions as c
from boolean_solver.code import Code
from boolean_solver.util import helpers
from constants import *

__author__ = 'juan pablo isaza'


def print_invoked_function(output):
    """
    Prints a function that is invoked with arguments: eg: fun(a, b)
    :param output: a c.Output object
    :return: string
    """
    if isinstance(output, c.Output):
        args_dict = output.arguments
        args_str = ''
        for var in helpers.get_function_inputs(output.function):
            if args_str == '':
                args_str += print_object(args_dict[var])
            else:
                args_str += ', ' + print_object(args_dict[var])

        return output.function.__name__ + '(' + args_str + ')'
    else:
        warnings.warn('method is not receiving correct data type', UserWarning)


def print_object(instance):
    """
    Modify output in special cases
    :param instance: anything to be printed as output code.
    :return: string with code representing the output
    """
    if isinstance(instance, str):
        return "\"{0}\"".format(str(instance))  # add ""

    if isinstance(instance, tuple):
        return str(instance)[1:-1]  # remove parenthesis.

    if helpers.is_function(instance):
        return instance.__name__  # when the function is passed as object; not invoked.

    if isinstance(instance, Code):
        return str(instance.code_as_str)

    if isinstance(instance, c.Output):
        return print_invoked_function(instance)

    return str(instance)


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
            indent + '        ' + r + print_object(output)]


def get_code_piece(bool_expression, indent, the_output):
    """
    Gives a line of code with a boolean expression and its return keyword, or an if statement.
    :param bool_expression: just booleans
    :param indent: function indent
    :param the_output: the value to be returned.
    :return: string list with code.
    """
    if isinstance(the_output, bool):
        return [indent + "    return " + bool_expression]
    else:
        return get_if_code(indent, bool_expression, the_output, True)


def get_initial_implementation(definition):
    """
    Always starts implementation with definition
    :param definition: function definition.
    :return: code
    """
    signature = get_signature(definition)
    indent = helpers.get_indent_from_definition(definition)

    return [indent + "def " + signature + ":"]


def add_code_to_implementation(current_implementation, bool_expression, definition, the_output):
    """
    Given definition and expression gets the function implementation.
    :param bool_expression: a boolean expression that can be evaluated.
    :param definition:   def function(input1, input2, ...).
    :return: string list with implementation.
    """
    signature = get_signature(definition)
    indent = helpers.get_indent_from_definition(definition)
    if bool_expression and len(bool_expression) > 0:

        new_code = get_code_piece(bool_expression, indent, the_output)
        return current_implementation + new_code
    else:
        warnings.warn('Function: ' + signature + ' has no boolean expression; cannot be implemented', UserWarning)
        return current_implementation


def get_signature(definition):
    """
    Gets the signature of a function given the definition ie: from:'    def sum(a, b):  #bla bla bla' to 'sum(a,b)'
    :param definition:
    :return: string signature.
    """
    signature_obj = re.search(FUNCTION_PATTERN, definition)
    if signature_obj is None:
        warnings.warn("Couldn't find signature of function")
        return None

    return signature_obj.group()


def print_input(instance):
    """
    Modify input in special cases
    :param instance: anything to be printed as output code.
    :return: string with code representing the input
    """
    if isinstance(instance, str):
        return instance

    if isinstance(instance, Code):
        return str(instance.code_as_str)

    return str(instance)


def translate_to_python_expression(all_inputs, qm_output):
    """
    Converts the algorithm output to friendlier python code.
    :param all_inputs: tuple with the names of the boolean inputs.
    :param qm_output: set containing strings. see "execute_qm_algorithm" for details.
    :return: python boolean expression
    """
    final_expression = ''

    for i, str_bits in enumerate(qm_output):

        factor = ''

        if i > 0:  # when more than one element on list, join by "or"
            final_expression += ' or '

        for j, character in enumerate(str_bits):

            if character != '-' and helpers.string_has_bits_for_and(str_bits, j):
                factor += ' and '

            if character == '1':
                factor += print_input(all_inputs[j])

            if character == '0':
                factor += 'not ' + print_input(all_inputs[j])

        final_expression += factor

    return final_expression
