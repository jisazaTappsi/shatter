BooleanSolver
=============

Introduction
------------

A picture is worth a thousand words and a vid is worth a thousand pictures, so watch a [short intro](https://youtu.be/w8tuJ9kqjJc) or continue reading...

This is a [python 3.6+ project](https://pypi.python.org/pypi/Boolean-Solver) to speed up boolean expression coding. Sometimes we need to crack a problem by combining boolean operators such as: `and`, `or` & `not`. We as humans are prone to err, specially when expressions get big. But there is an algorithm (Quine-McCluskey) to get this expressions with zero error. Just specify your specs in a test and set a dummy function on your code. When you run your tests a solver will take your specs and code them into a simple boolean expression, enjoy :).

This same boolean logic is being expanded to a broader range of problems; check other coding capabilities below.

Package Setup
-------------
1.  Install Boolean-Solver package:

        $ pip install Boolean-Solver

Short Example
-------------
Add new script(`start.py`) with a mock function:

    from mastermind import solver as s

    @s.solve()
    def and_function(a, b):
        pass

Add a unittest(`test.py`) with specs:

    import unittest
    from mastermind import solver
    import start
    
    
    class MyTest(unittest.TestCase):
        """
        1. Set rules of your function
        2. Run solve(callable, self) where callable is a function
         with the decorator=@solve().
         See examples below:
        """
        def test_AND_function(self):

            # The output is explicitly set to true
            cond = solver.Rules(a=True, b=True, output=True)
            cond.solve(self, start.and_function)

Then run `$ python -m unittest test`. In `start.py` the result should be:

    def and_function(a, b):
        return a and b

Non-Boolean outputs
-------------------

What if the output for a given logical condition is not a boolean. In that case a programmer would use an if. In the next example this package solves this case automatically:

Add `if_function(a, b)` to `start.py`:

    @s.solve()
    def if_function(a, b):
        pass
        
Add `test_ifs(self)` to `MyTest(unittest.TestCase)` class in `test.py`:
    
    def test_ifs(self):
        """
        Testing ifs.
        """
        cond = solver.Rules(a=False, b=True, output=1)  # non-boolean output
        cond.add(a=True, b=False, output=0)  # non-boolean output
        cond.solve(self, start.if_function)

Then run `$ python -m unittest test`, the result should be:

    def if_function(a, b):
    
        if not a and b:
            return 1
    
        if a and not b:
            return 0
    
        return False

Now, some cool coding
---------------------

Add `recursive(a)` to `start.py`:

    @s.solve()
    def recursive(a):
        pass

Add `test_recursive_function(self)` to `MyTest(unittest.TestCase)` class in `test.py`:
    
    def test_recursive_function(self):
        """
        Will do recursion, extremely cool!!!
        """
        args = {'a': solver.Code('not a')}
        out = solver.Output(start.recursive, args)

        cond = solver.Rules(a=False, output=0, default=out)
        cond.solve(self, start.recursive)

The result this time will be a recursive function :)

    def recursive(a):
    
        if not a:
            return 0
    
        return recursive(not a)

Expression behaving like boolean inputs
---------------------

Say you want to add a piece of code that evaluates to boolean, then:

Add `with_internal_code(a)` to `start.py`:

    @s.solve()
    def with_internal_code(a):
        pass

Add `test_internal_code(self)` to `MyTest(unittest.TestCase)` class in `test.py`:
    
    def test_internal_code(self):
        """
        Testing internal pieces of code
        """
        cond = solver.Rules(any_non_input_name=solver.Code('isinstance(a, str)'), output=2)
        cond.solve(self, start.internal_code)

The result should be:

    def internal_code(a):
    
        if isinstance(a, str):
            return 2
    
        return False

Source Code
-----------

Setup with source code
----------------------
1.  Clone repository:
    `git clone git@github.com:jisazaTappsi/BooleanSolver.git`

Intro Example with source code
------------------------------
1.  Enter `mastermind`:
    `cd mastermind`

2.  Run:
    `python start_sample.py`

        Sorry, run:
        python -m unittest test_sample
        first, to solve the riddle :)

3. So, run test with:
   `python -m unittest test_sample`

        Solved and tested and_function_3_variables
        .Solved and tested and_function
        .Solved and tested or_function
        .Solved and tested xor_function
        .
        ----------------------------------------------------------------------
        Ran 4 tests in 0.006s

        OK

4.  Run:
    `python start_sample.py`
    
          You made it, Congrats !!!
          Now, see the functions, enjoy :)

You just solved 4 boolean expressions: `and`, `or`, `xor` & `and3`. Specs for these functions are in `test_sample.py`.


How does Boolean Solver works?
------------------------------
Takes a function and a truth_table which is processed using the [Quine-McCluskey Algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm). Then finds a optimal boolean expression. This expression is inserted in the method definition with the decorator `@solve()`.

Arguments of `cond.solve(test, function)`
-------------------------------------------------------------------
1. The test case itself, to be able to perform tests, eg: `self`

2. A function to optimize, passed as a callable (with no arguments). This function needs a 3 mock line definition with:
    line 1: decorator = `@solve()`
    line 2: signature eg: `def my_function(a, b)`
    line 3: body: only one line, eg: `return False`. This line will be replaced by the boolean expression.

3. a. `solver.Rules()` instance: An object that can handle logical rules with named arguments eg:

        cond = solver.Rules(a=True, b=False)
    
        cond.add(a=True, b=True)

    The reserved word `output` allows:
    
        cond.add(a=False, b=False, output=False)
    
    Meaning that when `a=False, b=False` I want the `output` to be `False`

    b. Truth table: Alternatively a truth table can be specified (as a set containing tuples). Where each row is a tuple, the general form is:
    
        {tuple_row(tuple_inputs(a, b, ...), output), ...}
    
    or with a implicit `True` output:
     
        {tuple_inputs(a, b, ...), ...}

Arguments of `solver.Rules() and cond.add()`
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

`solver.Code`: Class that helps output pieces of code. The code is given as a String.

`solver.Solution`: Class that contains the solution of the problem it includes:
    
  - `rules`: The information given by the user.
  - `implementation`: Plain code.
  - `ast`: Abstract syntax tree
