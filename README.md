# BooleanSolver

## Introduction

This is a python project to help developers with boolean expressions during our coding. Sometimes we need to crack a problem by combining boolean operators such as: `and`, `or` & `not`. We as humans are prone to err, specially when expressions get big. Therefore there is an algorithm (Quine-McCluskey) to get this expressions with zero error. Just specify your specs in a test and set a dummy function on your code. When you run your tests a solver will take your specs and code them into a simple boolean expression, enjoy :).

## Instructions

### Intro Example

1.  Clone repository:
    `$ git clone git@github.com:jisazaTappsi/BooleanSolver.git`

2.  Install quine-mccluskey:
    `$ pip install quine-mccluskey`

3.  Then:
    `$ cd boolean_solver/`

4.  Run:
    `$ python start_sample.py`

        Sorry, run:
        $ python -m unittest test_sample
        first, to solve the riddle :)

5. So, run test with:
   `$ python -m unittest test_sample`

        Solved and tested and_function_3_variables
        .Solved and tested and_function
        .Solved and tested or_function
        .Solved and tested xor_function
        .
        ----------------------------------------------------------------------
        Ran 4 tests in 0.006s

        OK

6.  Run:
    `$ python start_sample.py`
    
          You made it, Congrats !!!
          Now, see the functions, enjoy :)

You just solved 4 boolean expressions: `and`, `or`, `xor` & `and3`. Specs for these functions are in `test_sample.py`. You can now add a new custom function with:

    @solve_boolean()
    def my_function(a, b):
        return False

And on `test_sample.py` add specs:

    def test_MY_function(self):
        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), True),
                       ((True, True), False)}
        solver.execute(self, functions1.and_function, truth_table)

Then run `$ python -m unittest test_sample` and see the result below `def my_function(a, b)`.