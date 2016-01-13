#!/usr/bin/env python

"""Defines a more user friendly way of entering data."""

import warnings
import util

__author__ = 'juan pablo isaza'


class Output():
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
        for var in util.get_function_inputs(function):
            if var not in arguments:
                return False

        return True

    def __init__(self, function, arguments):
        if self.valid_arguments(function, arguments):
            self.function = function
            self.arguments = arguments
        else:
            warnings.warn('function: ' + function.__name__ + ' has wrong arguments', UserWarning)


class Conditions(list):
    """
    It is a list that contains conditions, each being a dictionary with the inputs.
    """

    def __init__(self, **kwargs):
        list.__init__(list())

        if len(kwargs) > 0:
            self.add(**kwargs)

    def add(self, **kwargs):
        if len(kwargs) > 0:
            self.append(kwargs)
        else:
            warnings.warn('To add condition at least 1 argument should be provided', UserWarning)

    @staticmethod
    def get_tuples_from_indices(row, inputs):
        """
        Get a set containing tuples (with implicit or explicit rows).
        :param row: dict with index as key and value as input value.
        :param inputs: the output of the row.
        :return: set containing tuples.
        """
        out_str = 'output'

        def add_element_to_tuples(tuples_set, new_element):
            """
            Adds additional element to a tuple set.
            :param tuples_set: a set containing tuples.
            :param new_element: any element to add in last position.
            :return: tuple set
            """
            new_tuples = set()
            for tuple_element in tuples_set:
                new_tuples.add(tuple_element + (new_element,))

            return new_tuples

        #  -------------------------------------------------------

        if out_str in row:
            output = row[out_str]
            if isinstance(output, bool) and not output:
                return set()

        # starts with 1 tuple
        tuples = {()}
        for variable in inputs:

            if variable in row:
                tuples = add_element_to_tuples(tuples, row[variable])
            else:

                # All possible outcomes for undetermined boolean variable: duplicates number of tuples.
                true_tuples = add_element_to_tuples(tuples, True)
                false_tuples = add_element_to_tuples(tuples, False)
                tuples = true_tuples.union(false_tuples)

        # add explicit output to tuples, if necessary.
        return tuples

    @staticmethod
    def is_explicit(row):
        """
        Does the output is explicitly named on this table row. Has 2 elements the first is tuple.
        :param row: table row, or a condition.
        :return: boolean
        """
        return len(row) == 2 and isinstance(row[0], tuple)

    @staticmethod
    def get_output(row):

        out_str = 'output'
        out_args = 'output_args'
        if out_str in row and out_args in row:
            return Output(function=row[out_str], arguments=row[out_args])
        elif out_str in row:
            return row[out_str]

        return True

    def get_truth_tables(self, inputs):
        """
        Factor Truth tables by output.
        This is the 'private' version.
        :param inputs: variables.
        :return: dict(), where key=output and value=implicit truth table.
        """
        def change_keys_from_bool_to_int(d, new_key):
            """
            Changes the keys from booleans (True or False) to int(0 or 1)
            if a int(0 or 1) is present.
            :param d: dict
            :param new_key: a new key to be added to dict.
            :return: new dict
            """
            if util.var_is_1(new_key) and util.has_true_key(d):
                d[1] = d.pop(True, None)
            return d

        # dict where outputs are the keys, values are the rows.
        truth_tables = dict()

        for row in self:

            output = self.get_output(row)
            truth_tables = change_keys_from_bool_to_int(truth_tables, output)

            if output in truth_tables:
                truth_table = truth_tables[output]
            else:
                truth_table = set()

            condition_rows = self.get_tuples_from_indices(row, inputs)
            truth_table = truth_table.union(condition_rows)
            truth_tables[output] = truth_table  # add to tables dict.

        return truth_tables


def add_to_dict_table(table, key, value):
    """
    Converts the table from tuples (explicit or implicit) to a dict().
    Where the key is the output.
    :param table: dict
    :return: modified table
    """
    # will ignore key=False
    if key:
        if key in table:
            table[key] = table[key].union({value})
        else:
            table[key] = {value}

    return table


def from_raw_set_to_dict_table(conditions):
    """
    Convert raw case to general format.
    :param conditions: obj
    :return: dict where key is output and value is implicit truth table.
    """
    table = dict()
    for row in conditions:
        if Conditions.is_explicit(row):
            table = add_to_dict_table(table, row[1], row[0])
        else:
            table = add_to_dict_table(table, True, row)

    return table


def get_truth_tables(conditions, inputs):
    """
    This is the 'public' version of the class method with the same name.
    :param conditions: either a truth table or a conditions object.
    :return: truth table (ie set with tuples).
    """
    if isinstance(conditions, Conditions):
        return conditions.get_truth_tables(inputs)
    elif isinstance(conditions, set):  # raw set case.
        return from_raw_set_to_dict_table(conditions)
    else:
        warnings.warn('Found conditions that is not a set nor a Conditions object', UserWarning)
    return conditions


def valid_conditions(conditions):
    """
    Valid conditions must be sets, inherit from set or be a Conditions object.
    If conditions is a set: all rows have to be tuples or inherit from tuple.
    :param conditions: truth table or a conditions object.
    :return: boolean.
    """
    if not isinstance(conditions, set) and not isinstance(conditions, Conditions):
        warnings.warn('Truth table is not a set or a Conditions object', UserWarning)
        return False

    if isinstance(conditions, set):
        for row in conditions:
            if not isinstance(row, tuple):
                warnings.warn('A row in truth table is not a tuple', UserWarning)
                return False

            # when the output is explicit, check for 2 elements of outer tuple.
            if isinstance(row[0], tuple):
                if len(row) != 2:
                    warnings.warn('A row with explicit output in truth table has wrong format.', UserWarning)
                    return False

    return True
