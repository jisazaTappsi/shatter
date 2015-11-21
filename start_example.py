__author__ = 'juan pablo isaza'

from functions.functions1 import *

and_result = and_function(True, True)  # should be: 'True and True = True'
or_result = or_function(True, False)  # should be: 'True or False = True'
xor_result = xor_function(True, False)  # should be: 'True ^ False = True'

if and_function_3_variables(and_result, or_function, xor_result):  # should be True
    print "You made it, Congrats !!!"
    print "Now, go and see functions1.py, enjoy :)"
else:
    print "Sorry, run test1.py first, to solve the riddle :)"