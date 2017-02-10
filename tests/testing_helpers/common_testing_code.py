#!/usr/bin/env python

"""Common functions to several tests."""

import copy
import re

from shatter import constants as cts
from shatter.util import helpers as h

__author__ = 'juan pablo isaza'


def line_has_solve(line):
    """
    :param line
    :return: boolean
    """
    return re.search(cts.SOLVE_DECORATOR_PATTERN, line) is not None


def reset_functions_file(path, hard_reset=False):
    """
    All functions with @solver() decorator of a module are set to pass.
    :param path: of module
    :param hard_reset: if False will only reset the @solver() otherwise reset all functions
    :return: void
    """
    path = get_source_path(path)
    file_code = h.read_file(path)
    new_file_code = copy.copy(file_code)

    previous_line = ''
    for index, line in enumerate(file_code):

        definition_obj = re.search(cts.DEFINITION_PATTERN, line)
        if definition_obj is not None and (line_has_solve(previous_line) or hard_reset):

            indent = h.get_indent_from_definition(line)
            f_length = len(h.get_function_code(index, file_code))
            index = new_file_code.index(line)
            new_file_code = new_file_code[:index+1] + [indent + '    pass'] + new_file_code[index + f_length:]

        # if no white spaces assing a new last line. Because there can be line breaks between decorator and function.
        if line.strip() != '':
            previous_line = line

    h.rewrite_file(path, new_file_code)


def get_source_path(path):
    """
    If the path is for the .pyc, then removes the character 'c'.
    :param path: string
    :return: corrected path
    """
    if path[-1] == 'c':
        return path[:-1]
    return path
