
"""
>>> class C(object):
...     pass
...
>>> id(C()) == id(C())    # weird!
True
>>> C() is C()            # expected, call to "is" has references
False


Now for something weirder! now those instances of C() don't get the same memory address.
Probably because we have to allocate memory for the names 'a' and 'b'

  >>> a = id(C())           
  >>> b = id(C())
  >>> a == b
  False


Now for a medley of strangness:

  >>> 2 is 2
  True
  >>> 2 is (1+1)
  True

  >>> 1 is 2
  False

  >>> "" is ""
  True

  >>> a = ""
  >>> b = ""
  >>> a is b
  True

  >>> a = tuple()
  >>> b = tuple()
  >>> a is b
  True

  >>> a = ()
  >>> b = ()
  >>> a is b
  True

  >>> a = set()    # NOT SETS THOUGH!
  >>> b = set()
  >>> a is b
  False

  >>> b = (1,2)
  >>> a = (1,2)
  >>> a is b
  False

"""
