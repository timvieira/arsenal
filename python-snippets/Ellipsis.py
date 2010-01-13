class MyRange:
    def __init__(self, lst):
        self.lst = lst
    def __getitem__(self, x):

        print 'args:', x
        if not hasattr(x, '__iter__'):
            x = [x]
        if Ellipsis in x:
            return "poopy"
        else:
            return "peepee"


r = MyRange(list("abcdefghijklmnopqrstuvwxyz"))
print r[1, 2, 3, 10, ..., 15]
print r[1, 2:4:2, 3::, ::, 10, ...]

print r[...]
print r[::]

print r[1:2, 3:4, 10, 15]


