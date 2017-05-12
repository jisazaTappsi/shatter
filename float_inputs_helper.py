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

        if last_variable is None or 'and' in last_variable:  # starts new interval
            variables.append('{} < {}'.format(input_name, mean(input_var, last_input)))
        else:  # completes interval
            variables[-1] += ' and {} < {}'.format(input_name, mean(input_var, last_input))

    elif output and not last_output:  # from 0 to 1

        on_first_var = len(variables) == 1

        # or len(variables) > 0
        if last_variable is None or 'and' in last_variable or on_first_var:  # starts new interval
            variables.append('{} > {}'.format(input_name, mean(input_var, last_input)))
        else:  # completes interval
            variables[-1] += ' and {} > {}'.format(input_name, mean(input_var, last_input))

    return variables


def get_variables(df, input_name):

    variables = []
    last_output = None
    last_input = None
    for idx, row in df.iterrows():

        input_var = row[input_name]
        output = row['y']

        last_variable = get(variables, -1, None)

        if last_output is not None:
            variables = add_variable(variables, last_variable, input_var, output, last_input, last_output, input_name)

        last_output = output
        last_input = input_var

    return variables
