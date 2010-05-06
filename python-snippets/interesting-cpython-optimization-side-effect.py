# Here's something that surprised me:

a = None
def f():
    b = a
    return b
def g():
    b = a
    a = 'foo'
    return b

# While f() is perfectly fine, g() raises an UnboundLocalError. 
# This is because Python optimises access to local variables using the
# LOAD_FAST/STORE_FAST opcode, you can easily see why this is looking at the 
# code objects of those functions:

"""
>>> f.__code__ .co_names
()
>>> f.__code__ .co_varnames 
('a', 'b')
>>> g.__code__ .co_names
('a',)
>>> g.__code__ .co_varnames 
('b',)
"""

# I actually found out this difference thanks to finally watching the
# Optimizations And Micro-Optimizations In CPython talk by Larry Hastings
# from PyCon 2010. I never realised that you could create a situation where 
# the nonlocal scope would not be looked in.
