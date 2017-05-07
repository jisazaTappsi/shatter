Shatter
=============

Data driven programming; input data and output nice functional code ;)


Introduction
------------

This is a [python 3.6+ project](https://pypi.python.org/pypi/shatter) that uses algorithms to transform a set of
conditions into functional python code. See some [examples](https://github.com/jisazaTappsi/shatter/tree/master/examples).


Package Setup
-------------
1.  Install shatter package:

        $ pip install shatter


Short Example
-------------
Copy paste this snippet:

    from shatter.solver import Rules


    def my_func(a, b):
        pass
    
    r = Rules(a=True, b=True, output=True)
    r.solve(my_func)

Run it and see how `my_func` code changes from `pass` to `return a and b`. We just
specified that when `a` and `b` are true then the output should be `True`, that is equivalent to the
logical `and` operator.

We can add further conditions and `shatter` will compute the optimal function to get there.


Add more conditions:
-------------
Now we add 2 additional conditions with `r.add()`:

    from shatter.solver import Rules


    def my_func(a, b):
        pass
    
    
    r = Rules(a=True, b=True, output=True)
    r.add(a=False, b=True, output=True)
    r.add(a=True, b=False, output=True)
    r.solve(my_func)

In this case the solution is `a or b`.


If Conditionals
-------------------

What if the output for a given logical condition is not a boolean? In that case a programmer would use an if.
In the next example this package solves this case:

Change output to `1`:

    from shatter.solver import Rules


    def my_func(a, b):
        pass
    
    r = Rules(a=True, b=True, output=1)
    r.solve(my_func)


The solution will be:

    def my_func(a, b):

        if a and b:
            return 1
    
        return False

Returns `1` or `False` otherwise.


Cool stuff
---------------------

Run this code:

    from shatter.solver import Rules, Code, Output


    def recursive(a):
        pass
    
    a = Code()
    args = {'a': a + 1}
    out = Output(function=recursive, arguments=args)
    
    r = Rules(stopping_condition=  a > 2, output=a, default=out)
    solution = r.solve(recursive)

The result this time will be a recursive counting function :)

    def recursive(a):

        if a > 2:
            return a
    
        return recursive(a + 1)

With `a = Code()` variable `a` is initialized as a code piece. Then with

    args = {'a': a + 1}

A dictionary for the inputs of the `recursive` function is declared. Those inputs are fed into a `Output` object:

    out = Output(function=recursive, arguments=args)

After `out` is passed via `default` keyword when initializing the `Rules` object. This `default` keyword 
is used to override the last return statement of the `recursive` function.


Expression behaving like boolean inputs
---------------------

Say you want to add a arbitrary piece of code that evaluates to boolean, then:

    from shatter.rules import Rules
    from shatter.code import Code
    
    
    def any_code(a):
        pass
    
    r = Rules(condition=Code(code_str='isinstance(a, str)'), output=2)
    r.solve(any_code)

The result should be:

    def internal_code(a):
    
        if isinstance(a, str):
            return 2
    
        return False

Here the piece of code `isinstance(a, str)` was added as the if condition to output `2`

Source Code
-----------

Setup with source code
----------------------
1.  Clone repository:
    `git clone git@github.com:jisazaTappsi/shatter.git`

Examples
------------------------------
See the [examples](https://github.com/jisazaTappsi/shatter/tree/master/examples).


How does shatter work?
------------------------------
Takes a function and a truth table which is processed using the
[Quine-McCluskey Algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm).
Then finds an optimal boolean expression. This expression is inserted in the method definition.

Arguments of `Rules.solve(function, unittest=None)`
-------------------------------------------------------------------

1. A function to optimize, passed as a callable (with no arguments). This function needs a 3 mock line definition with:
    line 1: decorator = `@solve()`
    line 2: signature eg: `def my_function(a, b)`
    line 3: body: only one line, eg: `return False`. This line will be replaced by the boolean expression.

2. Test Case to be able to perform tests.
See [example](https://github.com/jisazaTappsi/shatter/tree/master/examples/with_tests)

3. a. `solver.Rules()` instance: An object that can handle logical rules with named arguments eg:

        r = solver.Rules(a=True, b=False)
    
        r.add(a=True, b=True)

    The reserved word `output` allows:
    
        r.add(a=False, b=False, output=False)
    
    Meaning that when `a=False, b=False` I want the `output` to be `False`

    b. Truth table: Alternatively a truth table can be specified (as a set containing tuples). Where each row is a tuple, the general form is:
    
        {tuple_row(tuple_inputs(a, b, ...), output), ...}
    
    or with a implicit `True` output:
     
        {tuple_inputs(a, b, ...), ...}

Arguments of `solver.Rules() and r.add()`
-------------------------------------------------------------------

These are specified as a dictionary containing certain keywords as well as the function inputs.

Keywords are:

`output`: Determines the value to be returned when the given condition is True.

`output_args`: Dictionary with the values for the arguments when output is a function.
 
`default`: Value returned when non of the rules are True.


Helper Classes
--------------

`solver.Output`: Class that helps define a function with arguments as an output. Has fields:
  
  - `function`: A callable object.
  - `arguments` Dictionary with the function inputs.

`solver.Code`: Class that helps output pieces of code. The code is fed as a string (with optinal arg str_code)
or it can be declared as variables. eg:

    from shatter.solver import Code
    a = Code()
    b = Code()
    print(a > b)

Will literally print string `a > b` rather than the objects or any result.

`solver.Solution`: Class that contains the solution of the problem it includes:
    
  - `rules`: The information given by the user.
  - `implementation`: Plain code.
  - `ast`: Abstract syntax tree
