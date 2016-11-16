#!/usr/bin/env python

"""Short example"""

from mastermind import solver as s
from mastermind.solver import Rules, Code, Output

__author__ = 'juan pablo isaza'


"""
1. Set rules of your function.
2. Run cond.solve(callable) where callable is a function
 with the decorator=@solve().
 See examples below:
"""


@s.solve()
def and_function(a, b):
    pass

# A simple and function.
cond = Rules(a=True, b=True, output=True)
cond.solve(and_function)


@s.solve()
def if_function(a, b):
    pass

# A function with an if statement.
cond = Rules(a=False, b=True, output=1)  # non-boolean output
cond.add(a=True, b=False, output=0)  # non-boolean output
cond.solve(if_function)


@s.solve()
def recursive(a):
    pass

# Will do recursion, extremely cool!!!
args = {'a': Code(code_str='not a')}
out = Output(recursive, args)
cond = Rules(a=False, output=0, default=out)
cond.solve(recursive)


@s.solve()
def internal_code(a):
    pass

# Will have a arbitrary piece of code inside.
cond = Rules(any_non_input_name=Code(code_str='isinstance(a, str)'), output=2)
cond.solve(internal_code)
