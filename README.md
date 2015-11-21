# BooleanSolver

## Introduction

This is a python project to help developers with boolean expressions during our coding. Sometimes we need to crack a problem by combining boolean operators such as: `and`, `or` & `not`. We as humans are prone to err, specially when expressions get big. Therefore there is an algorithm (Quine-McCluskey) to get this expressions with zero error. Just specify your specs in a test and set a dummy function on your code. When you run your tests a solver will take your specs and code them into a simple boolean expression, enjoy :).

## Instructions

### Intro Example

1.  Clone repository:
    `$ git clone git@github.com:jisazaTappsi/BooleanSolver.git`

2.  Run:
    `$ python start_example.py`

        Sorry, run test1.py first, to solve the riddle :)

3. So, run tests with: `$ python -m unittest discover`

        We have solved the riddle, go run start_example.py again!!!
        .......
        ----------------------------------------------------------------------
        Ran 7 tests in 0.016s
        
        OK

4.  Run: `$ python start_example.py`
    
          You made it, Congrats !!!
          Now, go and see functions1.py, enjoy :)

You just solved 4 boolean expressions on file `functions/functions1.py`: `and`, `or`, `xor` & `and3`. Specs for these functions are in `tests/test1.py`. You can now add a new custom function with:

    @solve_boolean()
    def my_function(a, b):
        return False

And on `tests/test1.py` add specs:

    def test_MY_function(self):
        #                  b1     b0   output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), True),
                       ((True, True), False)}
        solver.execute(self, functions1.and_function, truth_table)

Then run `test1.py` and see the result below `def my_function(a, b)`.



