#!/usr/bin/env python

"""Defines a more user friendly way of entering data."""

import warnings
import pandas as pd

from shatter.constants import *
from shatter.output import Output
from shatter.util import helpers
from shatter.util.ordered_set import OrderedSet
from shatter.util.code_dict import CodeDict
from shatter import solver
from shatter.util import helpers as h

__author__ = 'juan pablo isaza'


class Rules(list):
    """
    It is a list that contains rules, each being a dictionary with the inputs.
    """

    @staticmethod
    def gets_start_positional_idx(dictionary):
        """
        Gets the biggest index for a dictionary and add 1.
        :param dictionary: any dict
        :return: int
        """
        max_idx = 0
        has_key = False
        for key in dictionary:
            if isinstance(key, str) and re.match("^" + POSITIONAL_ARGS_RULE + "\d+$", key) is not None:
                has_key = True
                r = re.search("\d+$", key)
                candidate = int(r.group())
                if candidate > max_idx:
                    max_idx = candidate

        if has_key:
            return max_idx + 1
        else:
            return 0

    def get_max_positional_arg(self):
        """
        Gets the index for the next positional argument to start.
        :return: int.
        """
        max_arg = 0
        for d in self:
            candidate = self.gets_start_positional_idx(d)
            if candidate > max_arg:
                max_arg = candidate

        return max_arg

    def search_repeating_variable(self, value):
        """Tries to find if variable was already declared. If so outputs the original key else outputs None. Will
        exclude reserved words, as they are not variable declarations.
        :param value: a variable value. For example a Code object.
        :return : key of possible repeating variable or None
        """
        for d in self:
            for key in set(d.keys()) - set(KEYWORDS.values()):
                if d[key] == value:
                     return key
        return None

    def get_dicts(self, args, kwargs):
        """
        Big issue solved here. Adds args, to have positional args always in the same order as the user inputs.
        Therefore the user can have short circuiting for logical operators, by having inputs in the right order.
        :param args: positional args. Used when specific order required.
        :param kwargs: a common dict
        :return: a vector containing dicts (which as of python 3.6 preserves insertion order)
        """
        a_dict = dict()

        # Adds args
        start_idx = self.get_max_positional_arg()
        for idx, e in enumerate(args):

            if isinstance(e, pd.DataFrame):
                # TODO: implement

                list_of_dicts = []

                variables = list(e.columns.values)
                for index, row in e.iterrows():
                    new_dict = dict()
                    for var in variables:
                        new_dict[var] = row[var]

                    list_of_dicts.append(new_dict)

                return list_of_dicts
            else:

                repeating_var = self.search_repeating_variable(e)
                if repeating_var is None:  # first time: declares new value.
                    a_dict[POSITIONAL_ARGS_RULE + str(start_idx + idx)] = e
                else:  # has been previously declared.
                    a_dict[repeating_var] = e

        # Adds kwargs
        for k in kwargs.keys():
            a_dict[k] = kwargs[k]

        return [a_dict]

    def __init__(self, *args, **kwargs):
        """
        init and add new parameters if provided.
        :param kwargs:
        :return:
        """

        # TODO: add comment: what is this? Can still pass all tests without this.
        list.__init__(list())

        if len(args) + len(kwargs) > 0:
            self += self.get_dicts(args, kwargs)

    def add(self, *args, **kwargs):
        """
        Adds a new row condition.
        :param kwargs: dictionary like parameters.
        :return: void
        """
        if len(args) + len(kwargs) > 0:
            self += (self.get_dicts(args, kwargs))
        else:
            warnings.warn('To add condition at least 1 argument should be provided', UserWarning)

    @staticmethod
    def validate(function, rules):
        """
        Validates the entries, for solver()
        :param function: callable
        :param rules: rules object or table.
        """
        # if invalid raises exception.
        h.valid_function(function) and valid_rules(rules)

        f_path = h.get_function_path(function)

        if not h.os.path.exists(f_path):
            raise NotImplementedError("Function path {} not found.".format(f_path))

    def solve(self, function, unittest=None):
        """
        Solves puzzle given the restrains added. This is a method wrapper of solver.execute().
        :param function: the function to be coded.
        :param unittest: optional, the current test being run eg: 'self'.
        :return: Solution object.
        """
        self.validate(function, self)
        return solver.return_solution(f=function,
                                      rules=self,
                                      unittest=unittest)

    def get_input_values(self, f_inputs, output):
        """
        Scans the whole rules object looking for input values, adds them with the function inputs.
        :param f_inputs: function inputs.
        :param output: thing returned
        :return: All possible inputs that are not keywords.
        """
        remove_elements = KEYWORDS.values()

        f_inputs = list(f_inputs)
        input_values = []
        for row in self:
            if KEYWORDS[OUTPUT] in row and row[KEYWORDS[OUTPUT]] == output:
                keys = helpers.remove_list_from_list(row.keys(), f_inputs)
                keys = helpers.remove_list_from_list(keys, remove_elements)
                input_values += [row[k] for k in keys]

        return f_inputs + input_values

    def get_input_keys(self, f_inputs, output):
        """
        Scans the whole rules object looking for input keys. Will add inputs (such as code pieces), that are not
        explicitly declared as function inputs.
        Uses OrderedSet because order is very important. The order is:
        first the f_inputs (ordered from right to left), then args added on the condition object from right to left and
        top to bottom.
        Example:
        >>> out = -1

        >>> def f(a, b):
        >>>     return a + b

        >>> r = Rules(c=1, d=2, output=out)
        >>> r.add(x=3, y=4, output='other_stuff')
        >>> r.add(e=3, f=4, output=out)

        >>> cond.get_input_keys(helpers.get_function_inputs(f), out)
        >>> OrderedSet(['a', 'b', 'c', 'd', 'e', 'f'])

        :param f_inputs: function inputs.
        :param output: the output of the row.
        :return: All possible inputs that are not keywords.
        """
        # TODO: missing optional args(kwargs) of the input function.
        f_inputs = OrderedSet(f_inputs)
        new_inputs = OrderedSet()

        for row in self:
            if KEYWORDS[OUTPUT] in row and row[KEYWORDS[OUTPUT]] == output:
                new_inputs |= OrderedSet(row.keys()) - f_inputs  # adds inputs who are not already args.

        all_elements = f_inputs | new_inputs

        return all_elements - KEYWORDS.values()

    @staticmethod
    def add_element_to_tuples(tuples_set, new_element):
        """
        Adds additional element to a tuple list.
        :param tuples_set: a set containing tuples.
        :param new_element: any element to add in last position.
        :return: tuple set
        """
        new_tuples = list()
        for tuple_element in tuples_set:
            new_tuples.append(tuple_element + (new_element,))

        return new_tuples

    def get_tuples_from_args(self, row, function_args, output):
        """
        Get a list containing tuples (with implicit or explicit rows).
        :param row: dict with index as key and value as input value.
        :param function_args: function
        :param output: the output of the row.
        :return: set containing tuples.
        """

        # starts with 1 tuple
        tuples = [()]
        for variable in self.get_input_keys(function_args, output):

            if variable in row:
                tuples = self.add_element_to_tuples(tuples, row[variable])
            else:

                # All possible outcomes for undetermined boolean variable: duplicates number of tuples.
                true_tuples = self.add_element_to_tuples(tuples, True)
                false_tuples = self.add_element_to_tuples(tuples, False)
                tuples = true_tuples + false_tuples

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
        """
        Gets the output from a row.
        :param row: dict.
        :return: output function or output or True if not specified.
        """
        out_key = KEYWORDS[OUTPUT]
        args_key = KEYWORDS[OUTPUT_ARGS]
        if out_key in row and args_key in row:  # This case is encountered only when the output is a function.
            return Output(function=row[out_key], arguments=row[args_key])
        elif out_key in row:
            return row[out_key]

        return True

    @staticmethod
    def row_has_no_keyword_keys(row):
        """
        Boolean output indicating whether a row (dict) has no keyword keys.
        :param row: dict.
        :return: True if there is at least 1 input different from a keyword.
        """
        row_keys = set(row.keys())
        keyword_keys = set(KEYWORDS.values())
        return len(row_keys.difference(keyword_keys)) > 0

    @staticmethod
    def change_key_from_bool_to_int(d, new_key):
        """
        Changes the keys from booleans (True or False) to int(0 or 1)
        if a int(0 or 1) is present.
        :param d: dict
        :param new_key: a new key to be added to dict.
        :return: new dict
        """
        if helpers.var_is_1(new_key) and helpers.has_true_key(d):
            d[1] = d.pop(True, None)

        if helpers.var_is_0(new_key) and helpers.has_false_key(d):
            d[0] = d.pop(False, None)

        return d

    def add_truth_table(self, truth_tables, row, function_args):
        """
        Adds a new truth table to the dict of truth_tables.
        :param truth_tables: orderDict, where the key is the output and the inputs are a orderSet of values.
        :param row: 1 row of self.
        :param function_args: tuple
        :return: modified truth_tables.
        """
        output = self.get_output(row)

        if output in truth_tables:  # uses existing table.
            truth_table = truth_tables[output]
        else:  # adds new truth table
            truth_table = list()

        condition_rows = self.get_tuples_from_args(row, function_args, output)
        truth_table = truth_table + condition_rows  # concat lists.

        truth_tables[output] = truth_table  # add to tables dict.

        return self.change_key_from_bool_to_int(truth_tables, output)

    def get_truth_tables(self, function_args):
        """
        Factor Truth tables by output.
        This is the 'private' version.
        :param function_args: variables.
        :return: CodeDict(), where key=output and value=implicit truth table.
        """

        # dict where outputs are the keys, values are the rows.
        truth_tables = CodeDict()

        for row in self:
            if self.row_has_no_keyword_keys(row):
                truth_tables = self.add_truth_table(truth_tables, row, function_args)

        return truth_tables


def add_to_dict_table(table, key, value):
    """
    Converts the table from tuples (explicit or implicit) to a dict().
    Where the key is the output.
    :param table: dict
    :param key: to be added to dict
    :param value: to be added to dict
    :return: modified table
    """
    if key in table:  # add value to set in already existing key value pair.
        table[key] = table[key] + [value]
    else:  # create new key value pair.
        table[key] = [value]

    return table


def solve(function, rules, unittest=None):
    """
    This is the static version of rules.solve()
    :param function: the function to be coded.
    :param rules: Rules object or truth table. The table can be represented in 2 ways:

    Representation 1: Can be specified as a set containing tuples, where each table row is a tuple; general form is:

            {table_row_tuple(), ...}

        Where each table_row_tuple has inputs and an output:

            (tuple_inputs(a, b, ...), output)

    Representation 2: Another simpler way of representing a truth table is with an implicit `True` output:

            {tuple_inputs(a, b, ...), ...}

        Note: this representation is limited to outputs that are boolean, if not use Representation 1.

    :param unittest: optional, the current test being run eg: 'self'.
    :return: Solution object.
    """
    Rules.validate(function, rules)
    return solver.return_solution(f=function,
                                  rules=rules,
                                  unittest=unittest)


def from_raw_list_to_dict_table(rules):
    """
    Convert raw case to general format.
    :param rules: obj
    :return: dict where key is output and value is implicit truth table.
    """
    table = dict()
    for row in rules:
        if Rules.is_explicit(row):  # explicit case
            table = add_to_dict_table(table, row[1], row[0])
        else:  # implicit case
            table = add_to_dict_table(table, True, row)

    return table

TYPE_ERROR = 'type_error'
ROW_ERROR = 'row_error'
EXPLICIT_ROW_ERROR = 'explicit_row_error'


class RulesTypeError(TypeError):
    def __init__(self, error_object, error_type):
        if TYPE_ERROR == error_type:
            message = 'Rules variable is not a list nor a Rules object, but rather type {}'\
                .format(type(error_object))
        elif ROW_ERROR:
            message = '{} row in truth table is not a tuple'.format(error_object)
        elif EXPLICIT_ROW_ERROR:
            message = '{} row with explicit output in truth table has wrong format.'.format(error_object)
        else:
            message = 'unknown TypeError'

        super(RulesTypeError, self).__init__(message)


def get_truth_tables(rules, function_args):
    """
    This is the 'public' version of the class method with the same name.
    :param rules: either a truth table or a rules object.
    :param function_args: the arguments of the function.
    :return: truth table (ie set with tuples).
    """
    if isinstance(rules, Rules):
        return rules.get_truth_tables(function_args)
    elif isinstance(rules, list):  # raw list case.
        return from_raw_list_to_dict_table(rules)
    else:
        raise RulesTypeError(rules, TYPE_ERROR)


def valid_rules(rules):
    """
    Valid rules objects must be lists, inherit from list or be a Rules object.
    - list case:  When the input is a raw table. If rules is a list then all rows have to be tuples or inherit
    from tuple.
    - Rules case: When the input is a Rules object.
    :param rules: truth table or a rules object.
    :return: boolean.
    """

    if not isinstance(rules, list) and not isinstance(rules, Rules):
        raise RulesTypeError(rules, TYPE_ERROR)

    # only for list. Explicitly forbids Rules class as Rules class inherits from list and would be easily mistaken for a
    # standard list.
    if isinstance(rules, list) and not isinstance(rules, Rules):
        for row in rules:
            if not isinstance(row, tuple):
                raise RulesTypeError(row, ROW_ERROR)

            # when the output is explicit, check for 2 elements of outer tuple.
            if isinstance(row[0], tuple):
                if len(row) != 2:
                    raise RulesTypeError(row, EXPLICIT_ROW_ERROR)

    return True
