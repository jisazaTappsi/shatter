__author__ = 'juan pablo isaza'

import warnings
import os
import re
import constants as cts


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


def get_function_line_number(f, input_file_list):
    """
    This method has borrowed source code from inspect package. Because their solution
    didn't worked for decorated methods. Also the line number was off by 1.
    :param f: function.
    :param input_file_list: a file source code, each line is an array element.
    :return: the line of the file(starting in zero), 0 if not found!
    """

    if hasattr(f, cts.INTERNAL_FUNC_CODE):
        line = f.internal_func_code.co_firstlineno
    else:
        line = f.func_code.co_firstlineno

    function_def = re.compile(r'^(\s*def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')
    while line > 0:
        if function_def.match(input_file_list[line]):
            break
        line -= 1
    return line
