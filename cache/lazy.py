from types import GeneratorType

class lazy(object):
    """A decorator that converts a function into a lazy property.
    The function wrapped is called the first time to retrieve the
    result and then that result is used the next time you access
    the value. If the method is a generator, the value is stored
    as a list.

    Note: instances must have a `__dict__` attribute in order for
    this property to work. So no '__slots__' please.
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__.
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
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
