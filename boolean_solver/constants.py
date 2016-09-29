#!/usr/bin/env python

"""Cts to use on the project."""

import re

__author__ = 'juan pablo isaza'

INTERNAL_FUNC_CODE = 'internal_func_code'

COMMENT_PATTERN = re.compile(r"\s*(#.*)?$")
INDENT = re.compile(r"^\s*")

VARIABLE = re.compile(r"\s*\w+\s*")
NAME = re.compile(r"\w+\s*")
FUNCTION_PATTERN = re.compile(r"{name}\(({var}(,{var})*)?\)".format(name=NAME.pattern, var=VARIABLE.pattern))

DEFINITION_PATTERN = re.compile(r"{indent}def\s+{function}\s*:{comment}".format(indent=INDENT.pattern,
                                                                                function=FUNCTION_PATTERN.pattern,
                                                                                comment=COMMENT_PATTERN.pattern))

SOLVE_DECORATOR_PATTERN\
    = re.compile(r"{indent}@\s*({name}\.)?\s*solve\s*\(\){comment}".format(name=NAME.pattern,
                                                                           indent=INDENT.pattern,
                                                                           comment=COMMENT_PATTERN.pattern))


# reserved keywords
DEFAULT = 'DEFAULT'
OUTPUT = 'OUTPUT'
OUTPUT_ARGS = 'OUTPUT_ARGS'

KEYWORDS = {DEFAULT: 'default',
            OUTPUT: 'output',
            OUTPUT_ARGS: 'output_args'}

POSITIONAL_ARGS_RULE = "positional_args_rule_"
