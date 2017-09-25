#!/usr/bin/env python

"""Utility and General purpose functions."""
import inspect
import warnings
import os
import re

import shatter.constants as cts

__author__ = 'juan pablo isaza'


def read_file(absolute_path):
    """
    :param absolute_path: string path.
    :return: list with lines of the file.
    """
    return [line.rstrip('\n') for line in open(absolute_path)]


def delete_file(filename):
    """
    :param filename: relative path to file.
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True

    return False


def write_file(filename, the_list):
    """
    :param filename: relative path to file.
    :param the_list: new file information.
    :return: void
    """
    new_file = open(filename, 'a')

    for item in the_list:
        new_file.write("%s\n" % item)


def rewrite_file(filename, the_list):
    """
    Delete and write again
    :param filename: relative path to file.
    :param the_list: new file information.
    :return: void
    """
    delete_file(filename)
    write_file(filename, the_list)


def bit_in_string(string):
    """
    Contains a bit in the string
    :param string: arbitrary string
    :return: boolean
    """
    return ('0' in string) or ('1' in string)


def string_has_bits_for_and(str_bits, index):
    """
    Returns true if finds a bit, before and after index.
    :param index: int
    :param str_bits: string
    :return: boolean
    """
    str_start = str_bits[:index]
    str_end = str_bits[index:]
    return index > 0 and bit_in_string(str_start) and bit_in_string(str_end)


def from_bool_to_bit(boolean):
    """
    Conversion from boolean to bit
    :param boolean: True or False
    :return: '1' or '0'
    """
    if boolean:
        return "1"
    else:
        return "0"


def get_function_path(f):
    """
    Passes the internal func_code to a attribute called internal_code on the wrapper.
    Then we call the wrapper attribute which throws metadata of the internal function, and gets the path.
    :param f: function
    :return: path
    """
    # does the wrapper is defining the new attribute, to expose internal func_code? or use std func_code if no decorator
    code = f.internal_code if hasattr(f, cts.INTERNAL_CODE) else f.__code__
    return code.co_filename


def valid_function(f):
    """
    Validates function. Returns warning if it is not a function or it doesn't have a decorator.
    :param f: function
    :return: passes, raises warning or raises TypeError
    """
    if not hasattr(f, '__call__'):
        raise TypeError('{} is not a valid function.'.format(f))

    if not hasattr(f, cts.INTERNAL_CODE):
        warnings.warn('Function {} has no decorator, reading can be harder!!!'.format(f.__name__), UserWarning)

    return True


def get_function_line_number(f, file_code):
    """
    Returns first line number for decorated and un-decorated methods. -1 if not found.
    :param f: function.
    :param file_code: the code as a list where each element is a line.
    :return: the line of the file(starting in zero), 0 if not found!
    """
    for index, line in enumerate(file_code):

        pattern = re.compile(cts.PARTICULAR_DEFINITION.pattern.format(name=f.__name__))
        definition = re.search(pattern, line)
        if definition:
            return index

    return -1


def get_function_inputs(f):
    """
    Given function signatures gets the name of the function.
    :param f: a callable function
    :return: input names on a tuple.
    """
    if hasattr(f, cts.INTERNAL_PARAMETERS):
        # 'internal_parameters' is defined inside the solver() annotation, see solver.py for details.
        return f.internal_parameters
    else:
        return f.__code__.co_varnames


def get_function_code(start, file_code):
    """
    Gets the source code of function. Opt for not using
    inspect package because it doesn't work with decorators
    :param start: the starting line number, of the function
    :param file_code: the source file lines
    :return: code.
    """
    def not_space_nor_comment(line):
        return len(line.strip()) > 0 and line.strip()[0] != '#'

    def inside_function(line_indent, f_indent):
        return len(line_indent) > len(f_indent) + 3

    base_indent = re.search(cts.INDENT, file_code[start]).group()

    end = start
    for index, l in enumerate(file_code[start + 1:]):
        l_indent = re.search(cts.INDENT, l).group()

        # decides if adding to function is required: no black space or comment
        if not_space_nor_comment(l):
            if inside_function(l_indent, base_indent):
                end = index + start + 2  # only add code if non-comment or empty spaces are inside function
            else:
                # end of function if found lower indent that is not a blank space and not a comment
                break

    return file_code[start:end]


def var_is_true(var):
    """
    Returns True if var= True, else False. Remember here that 1 is a almost True value
    but in this case should return False.
    :param var: any variable.
    :return: boolean
    """
    return var and isinstance(var, bool)


def var_is_false(var):
    """
    Returns True if var = False, else False. Remember here that 1 is a almost True value
    but in this case should return False.
    :param var: any variable.
    :return: boolean
    """
    return not var and isinstance(var, bool)


def has_true_key(d):
    """
    Returns True only if it has a True value as key.
    Has to be done this way because Python confuses '0' and '1' with False and True.
    :param d: dict()
    :return: boolean
    """
    for key in d:
        if var_is_true(key):
            return True
    return False


def has_return(implementation, definition):
    """
    Finds if the implementation already has a return.
    :param implementation: array with code implementation
    :param definition: function definition
    :return: Boolean
    """
    last_line = implementation[-1]
    indent = get_indent_from_definition(definition)
    pattern = r"^{indent}    return".format(indent=indent)
    return re.search(pattern, last_line) is not None


def has_false_key(d):
    """
    Returns True only if it has a False value as key.
    Has to be done this way because Python confuses '0' and '1' with False and True.
    :param d: dict()
    :return: boolean
    """
    for key in d:
        if var_is_false(key):
            return True
    return False


def var_is_1(var):
    """
    Boolean if var is equal to 1 and not True.
    :param var: variable
    :return: boolean
    """
    if var and not isinstance(var, bool):
        return True
    return False


def var_is_0(var):
    """
    Boolean if var is equal to 0 and not False.
    :param var: variable
    :return: boolean
    """
    if not var and not isinstance(var, bool):
        return True
    return False


def get_indent_from_definition(definition):
    """
    Uses regex to get the indent
    :param definition: of a function
    :return: indent as string
    """
    return re.search(cts.INDENT, definition).group()


def is_function(f):
    """
    Is it a function?
    :param f: function
    :return: boolean
    """
    return hasattr(f, '__call__')


def remove_list_from_list(all_list, list_to_remove):
    """
    :param all_list: original list
    :param list_to_remove: elements that will be removed from the original list.
    :return: subtracted list
    """

    return [value for value in all_list if value not in list_to_remove]


def is_private_call():
    """
    Searches in the stack for places where the package is. If there is something then the
    function is being called privately from inside the package, otherwise it is called from outside the package.
    :return: boolean
    """
    p_name = '/{}/'.format(cts.PACKAGE_NAME)
    p = re.match(r'^.*' + p_name, inspect.stack()[0].filename).group()

    # the number 2 in 'inspect.stack()[2:]' is because we are not looking inside is_private_call() function nor one
    # level above it, where its suppose to tell us if that function is being called privately or publicly.
    return any(re.match(p, frame.filename) is not None for frame in inspect.stack()[2:])


def name_in_frame(var, frame):
    """
    Looks at the locals of the frame and searches in it for var.
    :param var: variable to get name from.
    :param frame: a inspect frame
    :return: list with strings.
    """
    callers_local_vars = frame.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = name_in_frame(var, fi.frame)
        if len(names) > 0:
            return names[0]
