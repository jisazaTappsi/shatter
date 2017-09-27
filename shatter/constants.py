#!/usr/bin/env python

"""Cts to use on the project."""

import re

__author__ = 'juan pablo isaza'

PACKAGE_NAME = 'shatter'
INTERNAL_CODE = 'internal_code'
INTERNAL_PARAMETERS = 'internal_parameters'

COMMENT_PATTERN = re.compile(r"\s*(#.*)?$")
INDENT = re.compile(r"^\s*")

VARIABLE = re.compile(r"\s*\w+\s*")
NAME = re.compile(r"\w+\s*")

ABSTRACT_FUNCTION = re.compile(r"{name}\(({var}(,{var})*)?\)".format(name='{name}', var='{var}'))

# TODO: add: "sync def function():" functions
ABSTRACT_DEFINITION = re.compile(r"{indent}def\s+{function}\s*:{comment}".format(indent='{indent}',
                                                                                 function='{function}',
                                                                                 comment='{comment}'))

FUNCTION_PATTERN = re.compile(ABSTRACT_FUNCTION.pattern.format(name=NAME.pattern, var=VARIABLE.pattern))
DEFINITION_PATTERN = re.compile(ABSTRACT_DEFINITION.pattern.format(indent=INDENT.pattern,
                                                                   function=FUNCTION_PATTERN.pattern,
                                                                   comment=COMMENT_PATTERN.pattern))

# leave name as placeholder
PARTICULAR_FUNCTION = re.compile(ABSTRACT_FUNCTION.pattern.format(name='{name}', var=VARIABLE.pattern))
PARTICULAR_DEFINITION = re.compile(ABSTRACT_DEFINITION.pattern.format(indent=INDENT.pattern,
                                                                      function=PARTICULAR_FUNCTION.pattern,
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
