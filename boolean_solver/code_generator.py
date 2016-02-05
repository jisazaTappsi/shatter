#!/usr/bin/env python

"""Generates pieces of code that are put together by solver.py"""

import warnings
from boolean_solver import util, conditions as c
from constants import *
from boolean_solver.code import Code

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
        for var in util.get_function_inputs(output.function):
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

    if util.is_function(instance):
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

    if isinstance(the_output, bool):
        return [indent + "    return " + bool_expression]
    else:
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
        return current_implementation + code
    else:
        return [current_implementation[0]] + code + current_implementation[1:]


def add_code_to_implementation(current_implementation, bool_expression, definition, the_output):
    """
    Given definition and expression gets the function implementation.
    :param bool_expression: a boolean expression that can be evaluated.
    :param definition:   def function(input1, input2, ...).
    :return: string list with implementation.
    """
    signature = get_signature(definition)
    indent = util.get_indent_from_definition(definition)
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
    signature_obj = re.search(FUNCTION_PATTERN, definition)
    if signature_obj is None:
        warnings.warn("Couldn't find signature of function")
        return None

    return signature_obj.group()


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