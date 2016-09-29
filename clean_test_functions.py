#!/usr/bin/env python

"""setup the python package.py"""

import fnmatch
import os

from tests.testing_helpers import common_testing_code

__author__ = 'juan pablo isaza'

# On this files will only reset functions with @solve() decorator.
SOFT_FILES = ['start.py', 'examples/bowling/start_bowling.py', 'boolean_solver/start_sample.py']

# On this files will reset every function.
HARD_FILES = []


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
    testing_files = find('*_functions.py', path)

    # soft reset.
    for a_file in SOFT_FILES:
        common_testing_code.reset_functions_file(a_file, hard_reset=False)

    # hard reset
    for a_file in testing_files + HARD_FILES:
        common_testing_code.reset_functions_file(a_file, hard_reset=True)

clean_functions()
