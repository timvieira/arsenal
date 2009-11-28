
from collections import namedtuple

# MULTIPLE INHERITANCE!
class Article4(namedtuple('Article',('title','author')), tuple, object):
    __slots__ = ()
    def __str__(self):
        return '<<<'.join(base.__repr__(self) for base in Article4.__bases__)


aaa = Article4(*('my-title','my-self'))
print aaa
