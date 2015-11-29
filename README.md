# BooleanSolver

## Introduction

This is a [python 2 project](https://pypi.python.org/pypi/Boolean-Solver/0.1.1#downloads) to speed up boolean expression coding. Sometimes we need to crack a problem by combining boolean operators such as: `and`, `or` & `not`. We as humans are prone to err, specially when expressions get big. But there is an algorithm (Quine-McCluskey) to get this expressions with zero error. Just specify your specs in a test and set a dummy function on your code. When you run your tests a solver will take your specs and code them into a simple boolean expression, enjoy :).

## Instructions

### Setup

1.  Clone repository:
    `$ git clone git@github.com:jisazaTappsi/BooleanSolver.git`

2.  Install quine-mccluskey package:
    `$ pip install quine-mccluskey`

### Intro Example

1.  Enter `boolean_solver`:
    `$ cd boolean_solver/`

2.  Run:
    `$ python start_sample.py`

        Sorry, run:
        $ python -m unittest test_sample
        first, to solve the riddle :)

3. So, run test with:
   `$ python -m unittest test_sample`

        Solved and tested and_function_3_variables
        .Solved and tested and_function
        .Solved and tested or_function
        .Solved and tested xor_function
        .
        ----------------------------------------------------------------------
        Ran 4 tests in 0.006s

        OK

4.  Run:
    `$ python start_sample.py`
    
          You made it, Congrats !!!
          Now, see the functions, enjoy :)

You just solved 4 boolean expressions: `and`, `or`, `xor` & `and3`. Specs for these functions are in `test_sample.py`.

### Short Example

You can now add a new custom function with:

    @solve_boolean()
    def my_function(a, b):
        return False

And on a test (for example on `test_sample.py`) add specs:

    def test_MY_function(self):
        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), True),
                       ((True, True), False)}
        solver.execute(self, functions1.and_function, truth_table)

Then run `$ python -m unittest test_sample` and see the result below `def my_function(a, b)`.

### How does Boolean Solver works?

Takes a function and a truth_table which is processed using the [Quine-McCluskey Algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm). Then finds a optimal boolean expression. This expression is inserted in the method definition with the decorator `@boolean_solver()`.

### Details

#### Arguments of `solver.execute(test, callable_function, truth_table)`

1. The test case itself, to be able to perform tests, eg: `self`

2. A function to optimize, passed as a callable (with no arguments). This function needs a 3 mock line definition with:
    line 1: decorator = `@solve_boolean()`
    line 2: signature eg: `def myfunction(a, b)`
    line 3: body: only one line, eg: `return False`. This line will be replaced by the boolean expression.

3. truth table is a set containing tuples. Where each row is a tuple the general form is:

    `{tuple_row(tuple_inputs(a, b, ...), output), ...}`
