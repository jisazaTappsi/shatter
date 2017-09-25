from shatter.constants import *


class Comparison:

    def __init__(self, a, b, operator):
        self.a = a  # number 1
        self.b = b  # number 2
        self.operator = operator  # '>=', '<=', '==' or 'and'

        # TODO: reactivate this, but first fix bug when making intervals (check them they suck)
        #self.simplify()

    def __str__(self):
        out = '{} {} {}'.format(self.a, self.operator, self.b)
        if self.is_composite():
            out = '({})'.format(out)
        return out

    def is_composite(self):
        return isinstance(self.a, Comparison) and isinstance(self.b, Comparison) and self.operator == 'and'

    def get_input(self):
        """
        Returns the variable, it's a string
        :return: string
        """
        return self.a.a if self.is_composite() else self.a

    def composite_has_opposing_operators(self):
        """
        Composite Comparison Objects, that have opposing operators (<=, >=)
        :return: Boolean
        """
        return self.a.operator == '>=' and self.b.operator == '<=' or self.a.operator == '<=' and self.b.operator == '>='

    def should_be_removed(self, my_range, percent_cut):
        """
        Calculates whether the current variable is too particular to consider for the percent cut demanded.
        :param my_range: absolute range of the variable
        :param percent_cut: percentage of absolute range below which the variable should be dropped from dataframe.
        :return: Boolean
        """

        if self.is_composite() and self.composite_has_opposing_operators():

            current_percentage = abs(self.a.b - self.b.b) / abs(my_range[0] - my_range[1])
            return current_percentage < percent_cut

        elif self.operator == '==' and percent_cut > 0:  # if equality
            return True

        return False

    def simplify(self):
        """
        It simplifies expressions like: x2 >= 3.25 and x2 <= 3.25   >>>  x2 == 3.25
        Because this statement is just the single number x2 = 3.25
        :return:
        """
        # it simplifies to an equality
        if self.is_composite() and self.a.b == self.b.b:

            self.a = self.a.a
            self.b = self.b.b
            self.operator = '=='


def get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


def mean(a, b):
    return (a+b)/2


def add_variable(variables, last_variable, input_var, output, last_input, last_output, input_name):
    """
    Adds or append boolean variable
    :param variables: array with boolean variables
    :param last_variable: the previous variable on the outer for iteration.
    :param input_var: input variable
    :param output: output variable
    :param last_input: the previous input variable on the outer for iteration.
    :param last_output: the previous output variable on the outer for iteration.
    :param input_name: string with name of input variable
    :return: variables list
    """

    if not output and last_output:  # from 1 to 0

        if last_variable is None or last_variable.operator == 'and':  # starts new interval
            variables.append(Comparison(input_name, mean(input_var, last_input), '<='))
        else:  # completes interval
            # TODO: Make intervals the Pythonic may, eg: 2.5 < b < 5.5
            comp2 = Comparison(input_name, mean(input_var, last_input), '<=')
            variables[-1] = Comparison(variables[-1], comp2, 'and')

    elif output and not last_output:  # from 0 to 1

        on_first_var = len(variables) == 1

        # or len(variables) > 0
        if last_variable is None or last_variable.operator == 'and' or on_first_var:  # starts new interval
            variables.append(Comparison(input_name, mean(input_var, last_input), '>='))
        else:  # completes interval
            comp2 = Comparison(input_name, mean(input_var, last_input), '>=')
            variables[-1] = Comparison(variables[-1], comp2, 'and')

    return variables


def get_variables(df, an_input):
    """
    Given a DataFrame and an_input it returns the associated conditions as variables.
    :param df: DataFrame
    :param an_input: string with an input.
    :return: list containing strings. Each string is a condition as well as a variable of the QM problem
    """
    variables = []
    last_output = None
    last_input = None
    for idx, row in df.iterrows():

        input_var = row[an_input]
        output = row[KEYWORDS[OUTPUT]]

        last_variable = get(variables, -1, None)

        if last_output is not None:
            variables = add_variable(variables, last_variable, input_var, output, last_input, last_output, an_input)

        last_output = output
        last_input = input_var

    return variables
