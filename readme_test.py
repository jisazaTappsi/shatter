#!/usr/bin/env python

"""setup the python package.py"""

from shatter.helpers import read_file
import os
import re
from subprocess import call


__author__ = 'juan pablo isaza'

# TODO: this didn't worked with the old readme as it was too complex, try with the new simpler one.


def has_code(line):
    return re.match(r'`.+`', line) or re.match(r'^    .+', line)


def get_code_pieces(line):

    code_line = re.match(r'^\s{4,}.+', line)

    if code_line:
        return [re.sub(r'^\s{4,}', '', code_line.group())]
    else:
        return re.findall(r"`(.+?)`+?", line)


def execute_code(code):

    for c in code:

        command = re.match(r'^\$.+', c)
        # executes command line.
        if command:
            call([re.sub(r'^\$.+', '', command.group())])
        # try creating new file.
        else:
            file_name = re.match(r'^.*\.py$', c)

            if file_name:
                call(['touch', file_name.group()])

            # try pasting to current working file.
            #else:


readme = read_file(os.getcwd() + '/README.md')

for l in readme:
    code = get_code_pieces(l)
    if code:
        execute_code(code)
