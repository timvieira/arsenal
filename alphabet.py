from flipdict import Flipdict

# TODO:
#  * use an array for the int->str mapping and dict for str->int
class Alphabet(object):
    def __init__(self):
        self.mapping = Flipdict()
        self.i = 0
        self.frozen = False
    def freeze(self):
        self.frozen = True
    def unfreeze(self):
        self.frozen = False
    @classmethod
    def from_iterable(cls, it):
        inst = cls()
        for x in it:
            inst[x]
        inst.freeze()
        return inst
    def lookup(self, i):
        assert isinstance(i, int)
        return self.mapping.flip[i]
    def __getitem__(self, k):
        try:
            return self.mapping[k]
        except KeyError:
            if not isinstance(k, str):
                raise InvalidKeyException("Invalid key (%s): only strings allowed." % k)
            if self.frozen:
                raise AssertionError('Alphabet is frozen and key (%s) was not found.' % k)
            self.mapping[k] = self.i
            self.i += 1
            return self.mapping[k]
    def __iter__(self):
        return iter(self.mapping)
    def __len__(self):
        return len(self.mapping)

class InvalidKeyException(Exception):
    pass
