__author__ = 'juan pablo isaza'
import os


def read_file(filename):
    """
    :param filename: relative path.
    :return: list with lines of the file.
    """
    return [line.rstrip('\n') for line in open(filename)]


def delete_file(filename):
    """
    :filename: relative path to file.
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True

    return False


def write_file(filename, the_list):
    """
    :param filename: relative path to file.
    :param the_list: new file information.
    :return: void
    """
    new_file = open(filename, 'a')

    for item in the_list:
        new_file.write("%s\n" % item)


def rewrite_file(filename, the_list):
    """
    Delete and write again
    :param filename: relative path to file.
    :param the_list: new file information.
    :return: void
    """
    delete_file(filename)
    write_file(filename, the_list)


def bit_in_string(string):
    """
    Contains a bit in the string
    :param string: arbitrary string
    :return: boolean
    """
    return ('0' in string) or ('1' in string)


def string_has_bits_for_and(str_bits, index):
    """
    Returns true if finds a bit, before and after index.
    :param index: int
    :param str_bits: string
    :return: boolean
    """
    str_start = str_bits[:index]
    str_end = str_bits[index:]
    return index > 0 and bit_in_string(str_start) and bit_in_string(str_end)


def from_bool_to_bit(boolean):
    """
    Conversion from boolean to bit
    :param boolean: True or False
    :return: '1' or '0'
    """
    if boolean:
        return "1"
    else:
        return "0"


def get_function_path(callable_function):
    """
    Passes the internal func_code to a attribute called internal_func_code on the wrapper.
    Then we call the wrapper attribute which throws metadata of the internal function, and gets the path.
    :return: path
    """
    code = callable_function.internal_func_code
    return code.co_filename
