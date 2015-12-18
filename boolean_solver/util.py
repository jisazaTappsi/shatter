__author__ = 'juan pablo isaza'

import warnings
import os
import imp
import sys

#import imp
#import site
#from boolean_solver import solver as prod_solver
#p = site.getsitepackages()[1]
#prod_solver = imp.load_source('boolean_solver.solver', '/Library/Python/2.7/site-packages')
#m = prod_solver.execute


def import_non_local_package(name, alias=None):

    alias = alias or name

    f, pathname, desc = imp.find_module(name, sys.path[1:])
    module = imp.load_module(alias, f, pathname, desc)
    f.close()

    return module


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
    code = f.internal_func_code if hasattr(f, 'internal_func_code') else f.func_code
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

    if not hasattr(f, 'internal_func_code'):
        warnings.warn('Function ' + f.func_name + ' has no decorator, reading can be harder!!!', UserWarning)

    return True