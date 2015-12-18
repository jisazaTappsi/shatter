__author__ = 'juan pablo isaza'

import warnings


class Conditions(list):

    def __init__(self):
        list.__init__(list())

    def add_condition(self, **kwargs):
        self.append(kwargs)

    @staticmethod
    def get_tuples_from_indices(row, inputs):
        """
        Get a set containing tuples (with implicit or explicit rows). Each
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

        def get_explicit_tuples(implicit_tuples, the_row):
            """
            gets set with tuples with explicit output.
            :param implicit_tuples: tuples only with inputs. No explicit output.
            :param the_row: the row containing all info.
            :return: set
            """
            if out_str in the_row:
                row_output = the_row[out_str]
                if not isinstance(row_output, bool):
                    new_tuples = set()

                    for a_tuple in implicit_tuples:
                        new_tuples.add((a_tuple, row_output))

                    return new_tuples

            return implicit_tuples

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
        return get_explicit_tuples(tuples, row)

    def get_set_with_tuples(self, inputs):
        """
        Gets the truth table for all cases, in the form af a set with tuples.
        :param inputs: variables.
        :return: set containing tuples.
        """
        truth_table = set()

        for row in self:

            condition_rows = self.get_tuples_from_indices(row, inputs)
            truth_table = truth_table.union(condition_rows)

        return truth_table


def valid_conditions(conditions):
    """
    Valid tables must be sets or inherit from set. And all rows have to be tuples or inherit from tuple.
    :param conditions: truth table or a conditions object.
    :return: boolean. true=valid, false=invalid
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