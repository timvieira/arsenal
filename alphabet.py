import re, sys, cPickle

## TODO:
##   add support for serializing the "alphabet" i.e. a bijective mapping from
##   feature names to unique indicies.
from flipdict import Flipdict
class Alphabet(object):
    def __init__(self, serialized=None):
        self.mapping = Flipdict()
        self.i = 1
        if serialized is not None:
            self.load(serialized)
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
    def save(self, f):
        cPickle.dump(self, file(f, 'wb'))
    def load(self, f):
        pkl = cPickle.load(file(f,'rb'))
        self.__dict__.update(pkl.__dict__)
