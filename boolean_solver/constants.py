#!/usr/bin/env python

"""Cts to use on the project."""

import re

__author__ = 'juan pablo isaza'

INTERNAL_FUNC_CODE = 'internal_func_code'

COMMENT_PATTERN = re.compile(r"\s*(#.*)?")
INDENT = re.compile(r"^\s*")

# TODO: add indent comment and function regex factoring
DEFINITION_PATTERN = re.compile(r"^\s*def\s*(\w+)\(\s*\w*\s*(,\s*\w+\s*)*\)\s*:")
FUNCTION_PATTERN = re.compile(r"(\w+)\(\s*\w*\s*(,\s*\w+\s*)*\)")
SOLVE_PATTERN = re.compile(r"{indent}^\s*@(\w+\.)?solve\(\){comment}".format(indent=INDENT.pattern,
                                                                             comment=COMMENT_PATTERN.pattern))


# reserved keywords
DEFAULT = 'DEFAULT'
OUTPUT = 'OUTPUT'
OUTPUT_ARGS = 'OUTPUT_ARGS'

KEYWORDS = {DEFAULT: 'default',
            OUTPUT: 'output',
            OUTPUT_ARGS: 'output_args'}

POSITIONAL_ARGS_RULE = "positional_args_rule_"
