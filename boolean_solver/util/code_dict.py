#!/usr/bin/env python

"""Works on top of orderDict to define a dictionary which compares Code object only by their content."""

from collections import OrderedDict, MutableMapping

from boolean_solver.code import Code

__author__ = 'Juan Pablo Isaza'


class CodeDict(MutableMapping):
    """Compare Code pieces by their content only"""

    def __init__(self, *args, **kwargs):
        self.store = OrderedDict()
        self.update(OrderedDict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):

        if isinstance(key, Code):

            for k, v in self.store.iteritems():
                if isinstance(k, Code) and key == k:
                    return self.store[k]
            raise KeyError
        else:
            return self.store[key]

    def __setitem__(self, key, value):

        if isinstance(key, Code):
            for k, v in self.store.iteritems():
                if isinstance(k, Code) and key == k:
                    self.store[k] = value
                    return

        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __contains__(self, item):
        if isinstance(item, Code):

            for value in self.store:
                if isinstance(value, Code) and item == value:
                    return True
            return False

        else:
            return item in self.store
