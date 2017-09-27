Shatter
=============

Data driven programming; input data and output nice functional code ;)


Introduction
=============

This is a [python 3.6+ project](https://pypi.python.org/pypi/shatter) that uses algorithms to transform a set of
conditions into functional python code. See some [examples](https://github.com/jisazaTappsi/shatter/tree/master/examples).


Package Setup
-------------

Install:

        $ pip install shatter


Dependencies
------------

    pyeda==0.28.0
    pandas==0.19.1
    sympy==1.1
    Keras==2.0.6
    numpy==1.13.1
    pip==9.0.1
    scikit_learn==0.19.0


Examples
=============


Get Started
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


Adding more conditions
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


If conditionals
-------------

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


Adding pieces of code
-------------

Say you want to add a arbitrary piece of code that evaluates to boolean, then:

    from shatter.solver import Rules, Code


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


Iteration
-------------

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


Solve Small ML problem
----------------------

Copy paste this snippet:

    import pandas as pd
    from sklearn import datasets
    from shatter.solver import Rules, solve


    @solve()
    def solve_iris(x1, x2, x3, x4):
        pass


    iris = datasets.load_iris()

    x = iris.data
    y = iris.target

    data_frame = pd.DataFrame(x, columns=['x1', 'x2', 'x3', 'x4'])

    # Make binary and add to df
    data_frame['output'] = [int(bool(e)) for e in y]


    print(data_frame)

    r = Rules(data_frame)

    solution = r.solve(solve_iris)


Outputs:

    def solve_iris():
        return x3 >= 2.45


Going deeper
=============

Setup
-------------

Clone repository:

    `git clone git@github.com:jisazaTappsi/shatter.git`

More examples
-------------

See [examples](https://github.com/jisazaTappsi/shatter/tree/master/examples).


How does shatter work?
-------------

Takes a function and a truth table which is processed using the
[Quine-McCluskey Algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm).
Then finds an optimal boolean expression. This expression is inserted in the method definition.


Rules Class
=============

Is initialized with one rule. Other rules can be added with `Rules.add()` method. To generate
the solution call `Rules.solve()` method.

Each rule
-------------

The arguments of each rule are specified as optional arguments inside a `Rules` constructor or inside a
`Rules.add()` call. There are reserved keywords:

`output`: Determines the value to be returned when the given condition is True.

`output_args`: Dictionary with the values for the arguments when output is a function.
 
`default`: Value returned when non of the rules are True.


Arguments of `Rules.solve()`
-------------

 - `function`: passed as a callable. This function is going to be filled with the solution to the present task.
 
 - `unittest=None`: Test Case to be able to run and test the code generated each time the test runs.
See [example](https://github.com/jisazaTappsi/shatter/tree/master/examples/with_tests) for a deeper understanding.


Output Class
-------------

`solver.Output`: Class that helps define a function with arguments as an output. Has fields:
  
  - `function`: A callable object.
  - `arguments` Dictionary with the function inputs.

Code class
-------------

`solver.Code`: Class that helps represent pieces of code. The code is fed as a string (with optional argument `str_code`)
or it can be declared as variables. eg:

    from shatter.solver import Code
    
    a = Code()
    b = Code()
    print(a > b)

This will literally print the code `a > b` rather than the objects or any result.


Solution class
-------------

`solver.Solution`: Class that contains the solution of the problem it includes:
    
  - `rules`: The information given by the user.
  - `implementation`: Plain code.
  - `ast`: Abstract syntax tree
