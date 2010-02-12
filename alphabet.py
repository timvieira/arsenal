import re, sys, cPickle as pickle

from flipdict import Flipdict
class Alphabet(object):
    def __init__(self):
        self.mapping = Flipdict()
        self.i = 0
        self.frozen = False
    def freeze(self):
        self.frozen = True
    def unfreeze(self):
        self.frozen = False
    def __getitem__(self, k):
        try:
            return self.mapping[k]
        except KeyError:
            if self.frozen:
                raise AssertionError('Alphabet is frozen and key (%s) was not found.' % k)
            self.mapping[k] = self.i
            self.i += 1
            return self.mapping[k]
    def __iter__(self):
        return iter(self.mapping)
    def __len__(self):
        return len(self.mapping)
