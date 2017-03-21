# based on  https://github.com/stucchio/Python-LRU-cache/blob/master/lru.py
from collections import OrderedDict

class LRU(object):
    """ A dictionary-like object, supporting LRU caching semantics.

    >>> d = LRU(max_size=3)
    >>> d['foo'] = 'bar'
    >>> d['foo']
    'bar'
    >>> d['a'] = 'A'
    >>> d['b'] = 'B'
    >>> d['c'] = 'C'
    >>> d['d'] = 'D'
    >>> d['a'] # Should return value error, since we exceeded the max cache size
    Traceback (most recent call last):
        ...
    KeyError: 'a'
    """
    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.__access_times = OrderedDict()

    def __len__(self):
        return len(self.__access_times)

    def clear(self):
        """
        Clears the dict.

        >>> d = LRU(max_size=3)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> d.clear()
        >>> d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        self.__access_times.clear()

    def __contains__(self, key):
        """
        This method should almost NEVER be used. The reason is that between the time
        has_key is called, and the key is accessed, the key might vanish.

        You should ALWAYS use a try: ... except KeyError: ... block.

        >>> d = LRU(max_size=3)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> 'foo' in d
        True
        >>> 'goo' in d
        False

        """
        return self.__access_times.has_key(key)

    def __setitem__(self, key, value):
        self.__access_times[key] = value
        self.cleanup()

    def __getitem__(self, key):
        return self.__access_times[key]

    def __delete__(self, key):
        del self.__access_times[key]

    def cleanup(self):
        #If we have more than self.max_size items, delete the oldest
        while (len(self.__access_times) > self.max_size):
            for k in self.__access_times.iterkeys():
                self.__delete__(k)
                break
