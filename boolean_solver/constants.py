#!/usr/bin/env python

"""Cts to use on the project."""

import re

__author__ = 'juan pablo isaza'

INTERNAL_FUNC_CODE = 'internal_func_code'
FUNCTION_PATTERN = re.compile(r"(\w+)\(\s*(\w*)(,\s*(\w+))*\)")
INDENT = re.compile(r"^\s*")
INITIAL_IMPLEMENTATION = []