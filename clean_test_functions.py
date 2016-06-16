#!/usr/bin/env python

"""setup the python package.py"""

import fnmatch
import os

from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'


def find(pattern, path):
    """
    Get list with file names that are in a given path with a given pattern
    :param pattern: regex
    :param path: just a path
    :return: list with paths.
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def clean_functions():
    """
    Cleans the auto generated functions, run before pushing.
    :return: void
    """
    path = os.path.dirname(os.path.abspath(__file__))
    path = '/'.join(path.split('/')) + '/tests/'
    res = find('*_functions.py', path)

    for a_file in res:
        common_testing_code.reset_functions_file(a_file)

clean_functions()
