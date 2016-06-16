#!/usr/bin/env python

"""This is the main file. Calls QM algorithm and code generation functions."""
import qm
from boolean_solver.solution import Solution
from boolean_solver.tester import test_implementation
from boolean_solver.util import helpers as h
from code_generator import *
from processed_conditions import *

#  TODO: from boolean_solver import solver as production_solver

__author__ = 'juan pablo isaza'

# TODO: add a decorator when function optimization is to be ignored. @ignore_solver()
# Maybe the programmer modified the original version and wants it to be manually specified.
# TODO: do the comment section of functions.
# TODO: Non specified output should be type dependant upon other outputs. For example:
# if outputs are of type string then non-specified default output should be ''.
# TODO: Add non returning outputs on ifs etc.
# TODO: Add internal code adding capabilities. Very important use code.py
# TODO: Add ast code verification to strings in Code.py
# TODO: missing a better tester test for table combination of arguments and Code objects


def solve():
    """
    This defines a Decorator, that will wrap the generated functions.
    :return: boolean value of generated function.
    """
    def wrap(f):
        """
        wrapper to be called at the end
        :param f: function
        :return: returns wrapped_f
        """
        # TODO: include optional **kwargs???
        def wrapped_f(*args):
            """
            same as wrap(f), but with *args
            :param args: of function
            :return: eval of f with args.
            """
            return f(*args)

        # Meta data transfer enables introspection of decorated functions.
        wrapped_f.__name__ = f.__name__
        wrapped_f.__module__ = f.__module__
        wrapped_f.internal_func_code = f.func_code

        return wrapped_f
    return wrap


def execute_qm_algorithm(ones):
    """
    Quine McCluskey algorithm.
    outputs the minimal boolean expression. Assumes that all none ones have a False output.
    :param ones: input combinations for which output is true
    :return: set containing lists of boolean expressions encoded as strings.
    Where: '1' = boolean ,'0' = not(boolean), '-' = don't care, '^^' = boolean0 ^ boolean1
    Example: set('1-','-0') = bit0 or not bit1
    """
    # TODO: cannot solve ones = ['00'] or a not(or(b0,b1))
    # TODO: change to True, add XOR logic
    qm_obj = qm.QuineMcCluskey(use_xor=False)
    return qm_obj.simplify_los(ones)


def get_function_expression(table, inputs):
    """
    Get boolean expression. Can return empty string.
    solution provided by mc algorithm.
    :param inputs: Function explicit inputs or implicit added rules.
    :param table: truth table.
    :return: string with boolean expression.
    """
    ones = from_table_to_ones(table)
    if len(ones) > 0:
        qm_output = execute_qm_algorithm(ones)
        return translate_to_python_expression(inputs, qm_output)
    else:
        return ''


def from_table_to_ones(table):
    """
    Gets the ones as a list of strings from a truth table like set, containing tuples.
    :param table: truth table
    :return: set containing bits.
    """
    ones = []
    for row in table:

        # case 1: when the output is explicit.
        if Conditions.is_explicit(row):
            if row[1]:  # only do it for true outputs.# TODO change for non booleans.
                ones.append(''.join(list(map(h.from_bool_to_bit, list(row[0])))))

        else:  # case 2: The output is a implicit True. inputs are in the row.
            ones.append(''.join(list(map(h.from_bool_to_bit, list(row)))))

    return ones


def alter_file(line_number, input_file_list, implementation, input_path):
    """
    Changes source file, when valid implementation found.
    :param line_number: of source.
    :param input_file_list: contains all lines of source.
    :param implementation: the new function.
    :param input_path: source file path.
    :return: void
    """
    source = h.get_function_code(line_number, input_file_list)

    input_file_list = input_file_list[:line_number] + implementation + input_file_list[line_number + len(source):]
    h.rewrite_file(input_path, input_file_list)


def get_empty_solution(function, conditions):
    """
    Wrapper to return an empty solution
    :param function: any function
    :param conditions: Conditions object.
    :return : solution object.
    """
    return Solution(implementation=[],
                    function=function,
                    conditions=conditions,
                    processed_conditions=ProcessedConditions())


def get_returning_implementation(implementation, definition, returning_value):
    """
    gets the code with the last default return.
    :param implementation: code
    :param definition: function definition
    :param returning_value: value to be returned
    :return: source code
    """
    indent = re.search(INDENT, definition).group()
    return implementation + ['', indent + '    return ' + print_object(returning_value)]


def add_default_return(definition, processed_conditions, implementation):
    """
    Modify source code to include a default return if no True key is present.
    :param definition: function def
    :param processed_conditions: obj containing dict with tables.
    :param implementation: source code
    :return: source code
    """
    if processed_conditions.default:
        return get_returning_implementation(implementation, definition, processed_conditions.default)
    elif not h.has_true_key(processed_conditions.tables):
        return get_returning_implementation(implementation, definition, False)

    return implementation


def get_input_values(conditions, function_inputs, output):
    """
    Adds to the original inputs other possible implicit inputs, such as code.
    :param conditions: Conditions obj
    :param function_inputs: explicit function inputs
    :param output: the output of the function.
    :return: a list with all the inputs.
    """
    if isinstance(conditions, Conditions):
        return conditions.get_input_values(function_inputs, output)
    else:  # when there is no conditions obj, then all inputs are explicitly named in the function.
        return list(function_inputs)


def return_solution(unittest, f, conditions):
    """
    Solves the riddle, Writes it and tests it.
    :param unittest: the unittest object that is passed to test stuff
    :param f: any function object.
    :param conditions: condition or object or partial truth table (explicit, implicit or mix).
    :return: True for successful operation, False if not.
    """
    f_path = h.get_function_path(f)
    file_code = h.read_file(f_path)
    f_line = h.get_function_line_number(f, file_code)

    # enters only if the function source code was found.
    if f_line > 0 and get_signature(file_code[f_line]):

        definition = file_code[f_line]
        function_inputs = h.get_function_inputs(f)

        # init variables
        implementation = get_initial_implementation(definition)
        processed_conditions = get_processed_conditions(conditions, function_inputs)

        for the_output, table in processed_conditions.tables.iteritems():

            all_inputs = get_input_values(conditions, function_inputs, the_output)
            expression = get_function_expression(table, all_inputs)

            if len(expression) > 0:
                implementation = add_code_to_implementation(current_implementation=implementation,
                                                            bool_expression=expression,
                                                            definition=definition,
                                                            the_output=the_output)

        implementation = add_default_return(definition, processed_conditions, implementation)
        solution = Solution(implementation=implementation,
                            function=f,
                            conditions=conditions,
                            processed_conditions=processed_conditions)
        test_implementation(unittest, solution)

        alter_file(f_line, file_code, implementation, f_path)
        print "Solved and tested " + f.__name__
        return solution

    return get_empty_solution(f, conditions)


def execute(unittest, function, conditions):
    """
    Solves the riddle, Writes it and tests it.
    :param unittest: the current test being run eg: 'self'.
    :param function: the function to be coded.
    :param conditions: condition or object or partial truth table (explicit, implicit or mix).
    :return: Solution object, empty object if operation unsuccessful.
    """
    # input validation
    if not h.valid_function(function) or not valid_conditions(conditions):
        return get_empty_solution(function, conditions)

    function = h.reload_function(function)
    f_path = h.get_function_path(function)

    if not h.os.path.exists(f_path):
        return get_empty_solution(function, conditions)

    return return_solution(unittest=unittest,
                           f=function,
                           conditions=conditions)
