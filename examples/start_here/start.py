#!/usr/bin/env python

"""Short example"""

from shatter import solver as s
from shatter.solver import Rules, Code, Output

__author__ = 'juan pablo isaza'


"""
1. Set rules of your function.
2. Run r.solve(callable) where callable is a function
 with the decorator=@solve().
 See examples below:
"""


@s.solve()
def and_function(a, b):
    pass

# A simple and function.
r = Rules(a=True, b=True, output=True)
r.solve(and_function)


@s.solve()
def if_function(a, b):
    pass

# A function with an if statement.
r = Rules(a=False, b=True, output=1)  # non-boolean output
r.add(a=True, b=False, output=0)  # non-boolean output
r.solve(if_function)


@s.solve()
def recursive(a):
    pass

# Will do recursion, extremely cool!!!
args = {'a': Code(code_str='not a')}
out = Output(recursive, args)
r = Rules(a=False, output=0, default=out)
r.solve(recursive)


@s.solve()
def internal_code(a):
    pass

# Will have a arbitrary piece of code inside.
r = Rules(any_non_input_name=Code(code_str='isinstance(a, str)'), output=2)
r.solve(internal_code)
