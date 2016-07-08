import numpy as np
from sys import stderr
from time import time
from contextlib import contextmanager
from arsenal.humanreadable import htime
from arsenal.terminal import yellow
from arsenal.misc import ddict

def timers(title=None):
    return Benchmark(title) #

class Benchmark(object):
    def __init__(self, title):
        self.title = title
        self.timers = ddict(Timer)
    def __getitem__(self, name):
        return self.timers[name]
    def compare(self):
        Timer.compare_many(*self.timers.values())
    def values(self):
        return self.timers.values()
    def keys(self):
        return self.timers.keys()
    def items(self):
        return self.timers.items()
    def __len__(self):
        return len(self.timers)
    def __iter__(self):
        return iter(sorted(self.keys()))
    def plot_feature(self, feature, timecol='timer', ax=None, **kw):
        if ax is None:
            import pylab as pl
            ax = pl.figure().add_subplot(111)
        for t in self.timers.values():
            t.plot_feature(feature=feature,
                           timecol=timecol,
                           ax=ax,
                           **kw)
        if self.title is not None:
            ax.set_title(self.title)
        ax.legend(loc=2)


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
        if len(self.times) <= 1:
            return 0.0
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
        for x in sorted(others, key=lambda x: x.name):
            if x != self:
                self.compare(x, **kw)

    def plot_feature(self, feature, timecol='timer', ax=None, show='avg', **kw):
        df = self.dataframe(timecol)
        a = df.groupby(feature).mean()

        loglog = kw.get('loglog')
        if 'loglog' in kw:
            del kw['loglog']

        if loglog:
            X = np.log(a.index)
            Y = np.log(a[timecol])
            ax.set_xlabel('log %s' % feature)
            ax.set_ylabel('log average time (seconds)')
        else:
            X = a.index
            Y = a[timecol]
            ax.set_xlabel(feature)
            ax.set_ylabel('average time (seconds)')

        if ax is None:
            import pylab as pl
            ax = pl.figure().add_subplot(111)

        if 'label' not in kw:
            # use name of the timer as default label.
            kw['label'] = self.name

        [l] = ax.plot(X, Y, lw=2, alpha=0.5, **kw)
        del kw['label'] # delete label so it doesn't appear twice in the legend

        if 'avg' in show:
            ax.scatter(X, Y, c=l.get_color(), lw=0, alpha=0.25, **kw)
        elif 'scatter' in show:
            if loglog:
                ax.scatter(np.log(df[feature]), np.log(df[timecol]), c=l.get_color(), alpha=0.25, **kw)
            else:
                ax.scatter(df[feature], df[timecol], c=l.get_color(), alpha=0.25, **kw)
        #elif 'box' in show:
        #    # TODO: doen't work very well yet. need to fill out the x-axis since
        #    # feature might not be dense. Should throw an error if feature isn't an
        #    # integral.
        #    ddd = [np.asarray(dd[timecol]) for f, dd in sorted(df.groupby(feature))]
        #    ax.boxplot(ddd)

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
def timeit(name, fmt='{name} ({htime})', header=None):
    """Context Manager which prints the time it took to run code block."""
    if header is not None:
        print header
    b4 = time()
    yield
    sec = time() - b4
    if sec < 60:
        ht = '%.4f sec' % sec
    else:
        ht = htime(sec)
    print >> stderr, fmt.format(name=name, htime=ht, sec=sec)

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
