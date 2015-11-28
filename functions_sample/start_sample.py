__author__ = 'juan pablo isaza'

from functions1 import *

and_result = and_function(True, True)  # should be: 'True and True = True', after running test1.
or_result = or_function(True, False)  # should be: 'True or False = True', after running test1.
xor_result = xor_function(True, False)  # should be: 'True ^ False = True', after running test1.

if and_function_3_variables(and_result, or_function, xor_result):  # should be True, after running test1.
    print "You made it, Congrats !!!"
    print "Now, go and see functions1.py, enjoy :)"
else:
    print "Sorry, run test1.py first, to solve the riddle :)"