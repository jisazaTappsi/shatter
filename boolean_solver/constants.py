#!/usr/bin/env python

"""Cts to use on the project."""

import re

__author__ = 'juan pablo isaza'

INTERNAL_FUNC_CODE = 'internal_func_code'
DEFINITION_PATTERN = re.compile(r"^\s*def\s*(\w+)\(\s*\w*\s*(,\s*\w+\s*)*\)\s*:")
FUNCTION_PATTERN = re.compile(r"(\w+)\(\s*\w*\s*(,\s*\w+\s*)*\)")
INDENT = re.compile(r"^\s*")
INITIAL_IMPLEMENTATION = []

# reserved keywords
DEFAULT_KEYWORD = 'default'
OUTPUT_KEYWORD = 'output'
OUTPUT_ARGS_KEYWORD = 'output_args'
