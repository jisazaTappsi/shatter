#!/usr/bin/env python

"""Common functions to several tests."""

import re
import copy

from boolean_solver import util as u
from boolean_solver import constants as boolean_cts

__author__ = 'juan pablo isaza'


def reset_functions_file(path):
    """
    All functions of a module are set to pass.
    :param path: of module
    :return: void
    """
    file_code = u.read_file(path)
    new_file_code = copy.copy(file_code)

    for index, line in enumerate(file_code):

        definition_obj = re.search(boolean_cts.DEFINITION_PATTERN, line)
        if definition_obj is not None:

            indent = u.get_indent_from_definition(line)
            f_length = len(u.get_function_code(index, file_code))
            index = new_file_code.index(line)
            new_file_code = new_file_code[:index+1] + [indent + '    pass'] + new_file_code[index + f_length:]

    u.rewrite_file(path, new_file_code)


def get_source_path(path):
    """
    If the path is for the .pyc, then removes the character 'c'.
    :param path: string
    :return: corrected path
    """
    if path[-1] == 'c':
        return path[:-1]
    return path