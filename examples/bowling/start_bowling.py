#!/usr/bin/env python

"""
http://code.joejag.com/coding-dojo/bowling-scores/
"""


from shatter.solver import solve


@solve()
def is_spare(frame):
    pass


@solve()
def is_strike(frame):
    pass


@solve()
def get_next_throw(i, game):
    pass


@solve()
def get_next_2_throws(i, game):
    pass


@solve()
def get_frame_score(frame, game, i):
    pass


@solve()
def recursive_get_score(game, i):
    pass


def get_score(game):
    """
    eg: game = ((10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,10,10))
    """

    # TODO: add recursive iteration and use solver for this.
    return recursive_get_score(game, 0)
