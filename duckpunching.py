"""
Duck punching: when things just don't quack right.
"""

import types

def monkeypatch_method(class_, name=None):
    '''
    Properly monkeypatch a method into a class.

    Example:

     >>> class A(object):
     ...     def my_method(a):
     ...         raise AssertionError

     >>> @monkeypatch_method(A)
     ... def my_method(a):
     ...     return 'wo0t!'

     >>> a = A()
     >>> assert a.my_method() == 'wo0t!'

    You may use the `name` argument to specify a method name different from the
    function's name.
    '''
    def decorator(function):
        # Note that unlike most decorators, this decorator retuns the function
        # it was given without modifying it. It modifies the class only.
        name_ = name or function.__name__
        setattr(class_, name_, types.MethodType(function, None, class_))
        return function
    return decorator

if __name__ == '__main__':
    import doctest
    doctest.testmod()
