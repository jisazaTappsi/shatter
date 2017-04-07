#!/usr/bin/env python

"""Defines a class containing possible outputs"""

from shatter.util import helpers

__author__ = 'juan pablo isaza'


class Output:
    """
    Contains any output properties.
    """
    @staticmethod
    def has_all_function_arguments(function, arguments):
        """
        Returns boolean indicating if all function arguments are in arguments input.
        :param function: object.
        :param arguments: dict with arguments.
        :return: Boolean.
        """
        # TODO: deal with optional arguments.
        function_args_tuple = helpers.get_function_inputs(function)
        return all(k in arguments for k in function_args_tuple)

    def __init__(self, function, arguments):
        if self.has_all_function_arguments(function, arguments):
            self.function = function
            self.arguments = arguments
        else:
            raise Exception("function named: '{}' has wrong or missing arguments.".format(function.__name__))
