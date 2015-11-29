BooleanSolver
=============

Introduction
------------
This is a [python 2 project](https://pypi.python.org/pypi/Boolean-Solver/0.1.1#downloads) to speed up boolean expression coding. Sometimes we need to crack a problem by combining boolean operators such as: `and`, `or` & `not`. We as humans are prone to err, specially when expressions get big. But there is an algorithm (Quine-McCluskey) to get this expressions with zero error. Just specify your specs in a test and set a dummy function on your code. When you run your tests a solver will take your specs and code them into a simple boolean expression, enjoy :).

Setup
-----
1.  Install quine-mccluskey package:
    `$ pip install quine-mccluskey`
    
2.  Install Boolean-Solver package:
    `$ pip install Boolean-Solver`
    
Short Example
-------------
Add new script(start.py) with a mock function:

    from boolean_solver import solver as s

    @s.solve_boolean()
    def and_function(a, b):
        return False

Add a unittest(test.py) with specs:

    import unittest
    from boolean_solver import solver
    import start
    
    
    class MyTest(unittest.TestCase):
        """
        1. Set the truth table of your boolean function (at least for rows where output=True)
        2. run solver.execute(self, callable, table) where callable is the boolean function
         with the decorator=@solve_boolean() in functions1.
         See examples below:
        """
        def test_AND_function(self):

        #                  b1     b0    output
        truth_table = {((False, False), False),
                       ((False, True), False),
                       ((True, False), False),
                       ((True, True), True)}

        solver.execute(self, start.and_function, truth_table)

Then run `$ python -m unittest test` and see the result below `def and_function(a, b)`.

How does Boolean Solver works?
------------------------------
Takes a function and a truth_table which is processed using the [Quine-McCluskey Algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm). Then finds a optimal boolean expression. This expression is inserted in the method definition with the decorator `@boolean_solver()`.

Arguments of `solver.execute(test, callable_function, truth_table)`
-------------------------------------------------------------------
1. The test case itself, to be able to perform tests, eg: `self`

2. A function to optimize, passed as a callable (with no arguments). This function needs a 3 mock line definition with:
    line 1: decorator = `@solve_boolean()`
    line 2: signature eg: `def myfunction(a, b)`
    line 3: body: only one line, eg: `return False`. This line will be replaced by the boolean expression.

3. truth table is a set containing tuples. Where each row is a tuple the general form is:

    `{tuple_row(tuple_inputs(a, b, ...), output), ...}`
