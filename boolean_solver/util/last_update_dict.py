#!/usr/bin/env python

"""Works on top of orderDict to define a dictionary which order depends on the order of last key update."""
from collections import OrderedDict, MutableMapping

__author__ = 'Juan Pablo Isaza'


class LastUpdateDict(MutableMapping):
    """Store items in the order the keys were last added"""

    def __init__(self, *args, **kwargs):
        self.store = OrderedDict()
        self.update(OrderedDict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            del self.store[key]
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
