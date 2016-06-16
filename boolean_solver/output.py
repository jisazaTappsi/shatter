#!/usr/bin/env python

"""Defines a class containing possible outputs"""

import warnings

from boolean_solver.util import helpers

__author__ = 'juan pablo isaza'


class Output:
    """
    Contains any output properties.
    """
    @staticmethod
    def valid_arguments(function, arguments):
        """
        Returns boolean indicating if all arguments are supplied.
        :param function: object.
        :param arguments: dict with arguments.
        :return: Boolean.
        """
        # TODO: deal with optional arguments.
        for var in helpers.get_function_inputs(function):
            if var not in arguments:
                return False

        return True

    def __init__(self, function, arguments):
        if self.valid_arguments(function, arguments):
            self.function = function
            self.arguments = arguments
        else:
            warnings.warn('function: ' + function.__name__ + ' has wrong arguments', UserWarning)
