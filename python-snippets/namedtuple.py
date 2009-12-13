from collections import namedtuple

# namedtuples dynamically create a class at RunTime via exec
Article = namedtuple('Article', ('title','author'), verbose=True)

a0 = ('mytitle', 'tim')
a1 = Article('mytitle', 'tim')
a2 = Article(*('mytitle', 'tim'))
a3 = Article(**{'author':'tim', 'title':'mytitle'})


def foo(*args):
    return args

a4 = foo(*a1)

assert a0 == a1 == a2 == a3 == a4

# this doesn't work tho...
try:
    def goo(**kwargs):
        print kwargs
    goo(**a1)
except TypeError, e:
    print 'OK: you can not **unpack a namedtuple (b/c it\'s not "a mapping")'


# BUT! you can create another "Article" with the fields slightly changed and yet equality does NOT work.
Article2 = namedtuple('Article', ('author','title'))

try:
    a6 = Article2('tim','mytitle')
    assert a6 == a1, "OK: permuting the field order changes the object... :-/"
except AssertionError, e:
    print e


Article3 = namedtuple('Article', ('title','author'))
a7 = Article3('mytitle','tim')
assert a7 == a1



