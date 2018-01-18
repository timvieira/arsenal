import numpy as np
import pylab as pl
import pandas
from collections import defaultdict
from arsenal.viz.util import update_ax

from arsenal.misc import ddict
lc = ddict(lambda name: LearningCurve(name))


class LearningCurve(object):
    """
    Plot learning curve as data arrives.
    """

    def __init__(self, name, sty=None, legend=True, averaging=True):
        self.name = name
        self.baselines = {}
        self.baselines_reward = {}
        self.data = defaultdict(list)
        self.sty = defaultdict(dict)
        if sty is not None:
            self.sty.update(sty)
        self.ax = None
        self.legend = legend
        self.averaging = averaging

    def plot(self):
        if self.ax is None:
            self.ax = pl.figure().add_subplot(111)
        ax = self.ax
        with update_ax(ax):
            sty = self.sty
            for k, v in self.baselines.items():
                ax.axhline(v, label=k, **sty[k])
            data = self.data
            for k, v in data.iteritems():
                xs, ys = np.array(data[k]).T

                if self.averaging:
                    sty[k]['alpha'] = 0.5

                [l] = ax.plot(xs, ys, label=k, **sty[k])
                # show a dot in addition to the line
                if 0:
                    s = sty[k].copy()
                    s['lw'] = 0
                    s['c'] = l.get_color()
                    ax.scatter(xs, ys, label=k, **s)

                if self.averaging:
                    s = pandas.Series(ys)

                    if 0:
                        halflife = 20
                        r = s.ewm(halflife=halflife)
                        M = r.mean()
                        s = r.std()
                        U = M + 2*s
                        L = M - 2*s
                    else:
                        window = min(len(ys), 10)
                        r = s.rolling(window, min_periods=0)
                        M = r.median()
                        #U = r.max()
                        #L = r.min()
                        U = r.quantile(.9)
                        L = r.quantile(.1)

                    ax.plot(xs, M, lw=2, c=l.get_color())
                    ax.fill_between(xs, U, L, color=l.get_color(), alpha=0.25)

            ax.set_title(self.name)
            if self.legend:
                ax.legend(loc='best')

    def update(self, iteration, **kwargs):
        "Update plots, if ``iteration is None`` we'll use ``iteration=len(data)``"
        data = self.data
        for k, v in kwargs.iteritems():
            i = len(data[k]) if iteration is None else iteration
            data[k].append([i, v])
        self.plot()

    def __reduce__(self):
        # Default pickle fails because of the reference to the plotting axis
        x = self.__dict__.copy()
        x['ax'] = None
        return (LearningCurve, (self.name, self.sty), x)
