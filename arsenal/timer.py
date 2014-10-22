import numpy as np
from time import time
from contextlib import contextmanager
from arsenal.humanreadable import htime
from arsenal.terminal import yellow
from arsenal.misc import ddict

def timers():
    return ddict(Timer)



class Timer(object):
    """
    >>> from time import sleep
    >>> a = Timer('A')
    >>> b = Timer('B')
    >>> with a:
    ...     sleep(0.5)
    >>> with b:
    ...     sleep(1)
    >>> a.compare(b)          #doctest:+SKIP
    A is 2.0018x faster

    """
    def __init__(self, name):
        self.name = name
        self.times = []
        self.features = []
        self.b4 = None

    def __enter__(self):
        self.b4 = time()

    def __exit__(self, *_):
        self.times.append(time() - self.b4)

    def __str__(self):
        return 'Timer(name=%s, avg=%g, std=%g)' % (self.name, self.avg, self.std)

    def __call__(self, **features):
        self.features.append(features)
        return self

    @property
    def avg(self):
        return np.mean(self.times)

    @property
    def std(self):
        return np.std(self.times, ddof=1)

    @property
    def total(self):
        return sum(self.times)

    def compare(self, other, attr='avg', verbose=True):
        if len(self.times) == 0 or len(other.times) == 0:
            print '%s %s %s' % (self.name, '???', other.name)
            return
        if getattr(self, attr) <= getattr(other, attr):
            print '%s is %6.4fx faster than %s %s' \
                % (self.name,
                   getattr(other, attr) / getattr(self, attr),
                   other.name,
                   ((yellow % '(%s: %s: %g %s: %g)' % (attr,
                                                      other.name, getattr(other, attr),
                                                      self.name, getattr(self, attr)))
                    if verbose else '')
                )
        else:
            other.compare(self, attr=attr, verbose=verbose)

    def compare_many(self, *others, **kw):
        for x in others:
            self.compare(x, **kw)

    def plot_feature(self, feature, timecol='timer', ax=None, **kw):
        a = self.dataframe(timecol).groupby(feature).mean()
        if ax is None:
            import pylab as pl
            ax = pl.figure().add_subplot(111)

        ax.plot(a.index, a[timecol], alpha=0.5, **kw)
        del kw['label']
        ax.scatter(a.index, a[timecol], lw=0, alpha=0.5, **kw)

        ax.set_xlabel(feature)
        ax.set_ylabel('average time (seconds)')
        return a

    def dataframe(self, timecol='timer'):
        from pandas import DataFrame
        df = DataFrame(list(self.features))
        df[timecol] = self.times
        return df

    def filter(self, f, name=None):
        t = Timer(name)
        t.times, t.features = zip(*[(x,y) for (x,y) in zip(self.times, self.features) if f(x,y)])
        return t


@contextmanager
def timeit(msg="%.4f seconds", header=None):
    """Context Manager which prints the time it took to run code block."""
    if header is not None:
        print header
    b4 = time()
    yield

    t = time() - b4
    ht = htime(t)
    if t < 60:
        ht = t
    try:
        print msg % ht
    except TypeError:
        print msg, ht

timesection = lambda x: timeit(header='%s...' % x,
                               msg=' -> %s took %%.2f seconds' % x)


def main():
    import pylab as pl
    from arsenal.iterview import iterview
    from time import sleep
    from numpy.random import uniform
    t = Timer('test')

    for i in iterview(xrange(1, 20)):
        for _ in xrange(10):
            with t(i=i):
                c = 0.01
                z = max(i**2 * 0.0001 + uniform(-c, c), 0.0)
                sleep(z)

    a = t.plot_feature('i')
    print a
    pl.show()


if __name__ == '__main__':
    main()
