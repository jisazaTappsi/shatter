#!/usr/bin/env python

"""cts to use on the tests"""

__author__ = 'juan pablo isaza'

#                b1     b0   output
and_table = [((False, False), False),
             ((False, True), False),
             ((True, False), False),
             ((True, True), True)]

# or table in reverse order, because of expression order and short circuiting
# (see test_rules_input_order_is_respected in code generator tests)
or_table = [((True, True), True),
            ((True, False), True),
            ((False, True), True),
            ((False, False), False)]

xor_table = [((True, True), False),
             ((True, False), True),
             ((False, True), True),
             ((False, False), False)]

nand_truth_table = [((False, False), True),
                    ((False, True), True),
                    ((True, False), True),
                    ((True, True), False)]

and3_table = [((True, True, True), True)]

sig_and = "and_function(a, b)"
exp_and = "a and b"
sig_or = "or_function(a, b)"
exp_or = "a or b"
sig_xor = "xor_function(a, b)"
exp_xor = "a and not b or not a and b"
sig_nand = "nand_function(a, b)"
exp_nand = "not a or not b"
sig_and3 = "and3_function(a, b, c)"
exp_and3 = "a and b and c"
