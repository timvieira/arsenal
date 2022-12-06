import numpy as np
from matplotlib import pyplot as pl
import pandas
from collections import defaultdict
from time import time

from arsenal.viz.util import update_ax
from arsenal.misc import ddict

class LearningCurve:
    """
    Plot learning curve as data arrives.
    """

    def __init__(self, name, sty=None, legend=True, ax=None):
        self.name = name
        self.baselines = {}
        self.data = defaultdict(list)
        self.sty = defaultdict(dict)
        if sty is not None:
            self.sty.update(sty)

        self.ax = pl.figure(figsize=(10,6)).add_subplot(111) if ax is None else ax
        self.legend = legend
        self.yscale = None
        self.xscale = None

        self.last_update = time()
        self.min_time = 0.5

        self.smoothing = None
        self._bands = None
        self.widget = None

    def smooth(self, type, aggregate, **kwargs):
        # TODO: look at notes:interpolated-signal for additional ideas for
        # smoothing the learning curve.
        if type == 'rolling':
            assert 'window' in kwargs
        elif type == 'ewm':
            assert 'half_life' in kwargs
        else:
            raise ValueError(self.smoothing.get('type'))
        self.smoothing = dict(type=type, aggregate=aggregate, **kwargs)
        self.add_widget()
        return self

    def bands(self, type):
        assert self.smoothing is not None
        self._bands = dict(type=type)
        return self

    def loglog(self):
        self.xscale = 'log'
        self.yscale = 'log'
        return self

    def semilogy(self):
        self.yscale = 'log'
        return self

    def semilogx(self):
        self.xscale = 'log'
        return self

    def draw(self):
        ax = self.ax
        with update_ax(ax):
            sty = self.sty
            for k, v in self.baselines.items():
                ax.axhline(v, label=k, **sty[k])
            data = self.data
            for k, v in data.items():
                xs, ys = np.array(data[k]).T

                if self.smoothing is not None:
                    # mute the raw signal when we are smoothing.
                    sty[k]['alpha'] = 0.5

                [l] = ax.plot(xs, ys, label=k, **sty[k])
                c = l.get_color()
                # show a dot in addition to the line
                if 0:
                    s = sty[k].copy()
                    s['lw'] = 0
                    s['c'] = c
                    ax.scatter(xs, ys, label=k, **s)

                self.draw_smoothing(xs, ys, c=c)
                self.draw_bands(xs, ys, c=c)

            if self.xscale: ax.set_xscale(self.xscale)
            if self.yscale: ax.set_yscale(self.yscale)
            if self.name:   ax.set_title(self.name)
            if self.legend: ax.legend(loc='best')

            ax = self.ax
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            #ax.spines['bottom'].set_visible(False)
            #ax.spines['left'].set_visible(False)

            self.draw_extra(ax)
            #self.ax.figure.tight_layout()

        return self

    def add_widget(self):
        if self.widget is not None: return
        from matplotlib.widgets import TextBox
        ax_widget = self.ax.figure.add_axes([0.1, .93, 0.06, 0.037])  # [left, bottom, width, height]

        def submit(text):
            if not text: return
            try:
                x = float(text)
                self.smoothing['half_life'] = x
                assert x > 0
            except (ValueError, AssertionError):
                print('bad value for smooting parameter')

        self.widget = TextBox(ax_widget, 'Smoothing ',
                              initial = str(self.smoothing['half_life']))

        self.widget.on_submit(submit)

    def draw_extra(self, ax):
        return

    def smoothed_signal(self, xs, ys):
        assert self.smoothing is not None
        s = pandas.Series(ys)
        if self.smoothing['type'] == 'ewm':
            # TODO: this doesn't use the distances in xs
            return s.ewm(halflife=self.smoothing['half_life'])
        elif self.smoothing['type'] == 'rolling':
            window = min(len(ys), self.smoothing['window'])
            return s.rolling(window, min_periods=0)

    def draw_smoothing(self, xs, ys, c):
        # Note: the smoothing happens on the original signal, not in log space.
        # We should probably add an option to smooth in log/log-log space.
        if self.smoothing is None: return
        r = self.smoothed_signal(xs, ys)
        if self.smoothing['aggregate'] == 'mean':
            zs = r.mean()
        if self.smoothing['aggregate'] == 'median':
            zs = r.median()
        self.ax.plot(xs, zs, lw=2, c=c)

    def draw_bands(self, xs, ys, c):
        if self._bands is None: return

        r = self.smoothed_signal(xs, ys)

        if self._bands['type'] == 'std':
            M = r.mean()
            s = r.std()
            U = M + 2*s
            L = M - 2*s

        if self._bands['type'] == 'quantile':
            U = r.quantile(.9)
            L = r.quantile(.1)

        self.ax.fill_between(xs, U, L, color=c, alpha=0.25)

    def update(self, iteration, **kwargs):
        "Update plots, if ``iteration is None`` we'll use ``iteration=len(data)``"
        return self._update(iteration, kwargs)

    def _update(self, iteration, kwargs):
        "Update plots, if ``iteration is None`` we'll use ``iteration=len(data)``"
        assert isinstance(kwargs, dict)
        data = self.data
        for k, v in kwargs.items():
            i = len(data[k]) if iteration is None else iteration
            data[k].append([i, v])
        if self.should_update():
            self.draw()
            self.last_update = time()
        return self

    def should_update(self):
        "Returns true if its been long enough (>= `min_time`) since the `last_update`."
        return time() - self.last_update >= self.min_time

    def __reduce__(self):
        # Default pickle fails because of the reference to the plotting axis
        x = self.__dict__.copy()
        x['ax'] = None
        return (LearningCurve, (self.name, self.sty), x)


lc = ddict(LearningCurve)



#def run():
#
#    lc = LearningCurve('test')
#    lc.smooth('ewm', 'mean', half_life = 0.01).bands('std')
#    for t in range(1, 1000):
#        lc.update(t, signal = np.exp(np.log(t) * -0.5 + np.random.randn()))
#        if t % 10 == 0:
#            lc.update(t, signal2 = np.exp(np.log(t) * -0.25 + np.random.randn()))
#        lc.loglog().draw()
#
#    pl.ioff(); pl.show()
#
#
#if __name__ == '__main__':
#    run()
#
