#!/usr/bin/env python

"""Works on top of orderDict to define a dictionary which order depends on the order of last key update."""

from collections import OrderedDict

__author__ = 'https://docs.python.org/2/library/collections.html#ordereddict-examples-and-recipes'


class LastUpdatedOrderedDict(OrderedDict):
    """Store items in the order the keys were last added"""

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)