#!/usr/bin/env python

"""Utility and General purpose functions."""

import warnings
import os
import re
import constants as cts

__author__ = 'juan pablo isaza'


def read_file(filename):
    """
    :param filename: relative path.
    :return: list with lines of the file.
    """
    return [line.rstrip('\n') for line in open(filename)]


def delete_file(filename):
    """
    :filename: relative path to file.
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
    Passes the internal func_code to a attribute called internal_func_code on the wrapper.
    Then we call the wrapper attribute which throws metadata of the internal function, and gets the path.
    :param f: function
    :return: path
    """
    # does the wrapper is defining the new attribute, to expose internal func_code? or use std func_code if no decorator
    code = f.internal_func_code if hasattr(f, cts.INTERNAL_FUNC_CODE) else f.func_code
    return code.co_filename


def valid_function(f):
    """
    Validates function. Returns warning if it is not a function or it doesn't has a decorator.
    :param f: function
    :return: boolean
    """
    if not hasattr(f, '__call__'):
        warnings.warn('callable_function argument is NOT a function.')
        return False

    if not hasattr(f, cts.INTERNAL_FUNC_CODE):
        warnings.warn('Function ' + f.func_name + ' has no decorator, reading can be harder!!!', UserWarning)

    return True


def get_function_line_number(f):
    """
    Returns first line number for decorated and un-decorated methods.
    :param f: function.
    :return: the line of the file(starting in zero), 0 if not found!
    """
    # decorated
    if hasattr(f, cts.INTERNAL_FUNC_CODE):
        # although co_firstlineno starts at 1 the decorator sums up 1.
        line = f.internal_func_code.co_firstlineno
    else:  # not decorated
        # co_firstlineno starts at 1 instead of 0
        line = f.func_code.co_firstlineno - 1

    #function_def = re.compile(r'^(\s*def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')
    #while line > 0:
    #    if function_def.match(input_file_list[line]):
    #        break
    #    line -= 1
    return line


def get_function_inputs(f):
    """
    Given function signatures gets the name of the function.
    :param f: a callable function
    :return: input names on a tuple.
    """
    if hasattr(f, cts.INTERNAL_FUNC_CODE):
        return f.internal_func_code.co_varnames
    else:
        return f.func_code.co_varnames


def get_function_code(start, lines):
    """
    Gets the source code of function. Opt for not using
    inspect package because it doesn't work with decorators
    :param start: the starting line, of the function
    :param lines: the source file lines
    :return: code.
    """
    def not_space_nor_comment(line):
        return len(line.strip()) > 0 and line.strip()[0] != '#'

    def inside_function(line_indent, f_indent):
        return len(line_indent) > len(f_indent) + 3

    base_indent = re.search(cts.INDENT, lines[start]).group()

    end = start
    for index, l in enumerate(lines[start + 1:]):
        l_indent = re.search(cts.INDENT, l).group()

        # decides if adding to function is required: no black space or comment
        if not_space_nor_comment(l):
            if inside_function(l_indent, base_indent):
                end = index + start + 2  # only add code if non-comment or empty spaces are inside function
            else:
                # end of function if found lower indent that is not a blank space and not a comment
                break

    return lines[start:end]


def var_is_true(var):
    """
    Returns True if var= True, else False. Remember here that 1 is a almost True value
    but in this case should return False.
    :param var: any variable.
    :return: boolean
    """
    return var and isinstance(var, bool)


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


def var_is_1(var):
    """
    Assert if var is equal to 1 and not True.
    :param var: variable
    :return: boolean
    """
    if var and not isinstance(var, bool):
        return True
    return False