from types import GeneratorType

class lazy(object):
    """
    Lazily load a property defined by a method. The method wrapped is called
    at most once to retrieve the result and the result is reused. If the method
    is a generator, the value is stored as a list.

    Note: instances must have a `__dict__` attribute in order for this property
    to work, i.e. no '__slots__' class attribute.

    Implementation detail: this is not implemented as a data descriptor so that
    we can completely avoid the function call overhead. If one choses to invoke
    `__get__` by hand the property will still work as expected because the 
    lookup logic is replicated in `__get__` for manual invocation.
    """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, type_=None):
        if obj is None:
            return self
        try:
            value = obj.__dict__[self.__name__]
        except KeyError:
            value = self.func(obj)
            if isinstance(value, GeneratorType):   # store generators as lists
                value = list(value)
            obj.__dict__[self.__name__] = value
        return value

    def __set__(self, obj, value):
        raise NotImplementedError

    def __delete__(self, obj):
        raise NotImplementedError
