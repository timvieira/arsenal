from os import environ
DISPLAY = True
if not environ.get('DISPLAY'):
    import matplotlib
    #print 'Not a display environment.'
    matplotlib.use('Agg')
    DISPLAY = False

import pandas as pd, numpy as np
import matplotlib.pyplot as pl
#from sys import stderr
from collections import defaultdict
from contextlib import contextmanager
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
from arsenal import colors
#from arsenal.viz.covariance_ellipse import covariance_ellipse
from arsenal.misc import ddict


#from palettable.colorbrewer import qualitative


simple_palette = ['r','g','b','y','c','m','k']
#default_palette = np.array(qualitative.Set1_6.mpl_colors)


#def name2color(palette = default_palette):
def name2color(palette = simple_palette):
    "Create a mapping from names to matplotlib colors."
    palette = list(palette)
    i = -1
    n = len(palette)
    def next_color():
        nonlocal i
        i += 1
        return palette[i % n]
    return defaultdict(next_color)


def save_plots(pdf):
    "save all plots to pdf"
    pp = PdfPages(pdf)
    for i in pl.get_fignums():
        pl.figure(i)
        pl.savefig(pp, format='pdf')
    pp.close()
    print(colors.yellow % 'saved plots to "%s"' % pdf)


# global reference to all of the plots
def newax():
    return pl.figure().add_subplot(111)
AX = defaultdict(newax)
DATA = defaultdict(list)


# TODO: [2018-04-18 Wed] Add support for visualizing constraints. Apparently,
# I'm constantly plotting constraints these days.
#
#  - There may be better ways to implement this (better defaults at least)
#
#    - Look into rasbt's decision boundary plotting script for some example usage of all these things.
#       https://github.com/rasbt/mlxtend/blob/62aea2a9fb6fafdecedfa041a2121c002e47dac9/mlxtend/plotting/decision_regions.py
#
#    - figure out the difference between contoutr/contourf)
#
#    - Look into value interpolation strategies
#      https://matplotlib.org/gallery/images_contours_and_fields/triinterp_demo.html#sphx-glr-gallery-images-contours-and-fields-triinterp-demo-py.
#
#    - For constraints look at value mask:
#      https://matplotlib.org/gallery/images_contours_and_fields/contour_corner_mask.html#sphx-glr-gallery-images-contours-and-fields-contour-corner-mask-py
#
# - For rendering constraints, we might want to use hatching instead of
#   something opaque.
#
def contour_plot(f, xdomain, ydomain, color='viridis', alpha=0.5, levels=None, ax=None):
    "Contour plot of a function of two variables."
    from arsenal import iterview
    if ax is None: ax = pl.gca()
    [xmin, xmax, _] = xdomain; [ymin, ymax, _] = ydomain
    X, Y = np.meshgrid(np.linspace(*xdomain), np.linspace(*ydomain))
    Z = np.array([f(np.array([x,y])) for (x,y) in iterview(zip(X.flat, Y.flat), length=len(X.flat))]).reshape(X.shape)
    contours = ax.contour(X, Y, Z, 20, colors='black', levels=levels)
    ax.clabel(contours, inline=True, fontsize=8)
    if color is not None:
        ax.imshow(Z, extent=[xmin, xmax, ymin, ymax], origin='lower', cmap=color, alpha=alpha)
        #ax.axis(aspect='scalar')
    ax.figure.tight_layout()
    ax.set_xlim(xmin,xmax); ax.set_ylim(ymin,ymax)

# TODO: No need to say "plot" we're already in a module called "viz". The whole
# point is reduce clutter when plotting.
contour = contour_plot

# TODO: Create an alias which case-analyzes and plots 3d vs 2d accordingly?
# TODO: also support interactive sliders and animation for when there are more parameters. use the same range notation.
def plot3d(f, xdomain, ydomain, ax=None):
    "3d surface plot of a function of two variables."
    #[xmin, xmax, _] = xdomain; [ymin, ymax, _] = ydomain
    X, Y = np.meshgrid(np.linspace(*xdomain), np.linspace(*ydomain))
    Z = np.array([f(np.array([x,y])) for (x,y) in zip(X.flat, Y.flat)]).reshape(X.shape)
    ax = pl.figure().gca(projection='3d') if ax is None else ax
    ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True)
    return ax


class plot_xsection:
    def __init__(self, f, a, b, n, ax=None, opts=None):
        """
        Plot a cross section of `f` by interpolating from `x0 to `x1` by `n`
        evenly space points.
        """
        if opts is None: opts = {}
        if ax is None: ax = pl.gca()
        self.n = n
        self.a = a
        self.b = b
        self.ts = np.linspace(0,1,n)
        self.fs = [f(xt) for xt in self.curve()]
        ax.plot(self.ts, self.fs, **opts)
        ax.set_xlabel('interpolation coefficient')
        self.ax = ax

    def __call__(self, f, opts=None):
        return plot_xsection(f=f, a=self.a, b=self.b, n=self.n, ax=self.ax, opts=opts)

    def curve(self):
        "Sweep a curve in parameter spaces which is convex combination of `a` and `b`."
        for t in self.ts:
            yield self.a*(1-t) + self.b*t


class NumericalDebug:
    """Incrementally builds a DataFrame, includes plotting and comparison method.

    The quickest way to use it is

      >>> from arsenal.viz import DEBUG
      >>> d = DEBUG['test1']
      >>> d.update(want=1, have=1)
      >>> d.update(want=1, have=1.01)
      >>> d.update(want=1, have=0.99)
         want  have
      0     1  1.00
      1     1  1.01
      2     1  0.99

    To plots and runs numerical comparison tests,

      >>> d.compare()     # doctest: +SKIP

    """

    def __init__(self, name):
        self.name = name
        self._data = []
        self._df = None
        self.ax = None
        self.uptodate = True

    @property
    def df(self):
        "lazily make DataFrame from _data."
        if not self.uptodate:
            self._df = pd.DataFrame(self._data)
        self.uptodate = True
        return self._df

    def update(self, **kw):
        "Pass in column values for the row by name as keyword arguments."
        self._data.append(kw)
        self.uptodate = False
        return self

    def compare(self, want='want', have='have', show_regression=1, scatter=1, **kw):
        from arsenal.maths import compare
        if self.ax is None:
            self.ax = pl.figure().add_subplot(111)
        if self.df.empty:
            return
        with update_ax(self.ax):
            compare(want, have, data=self.df).plot(ax=self.ax, **kw)

# Global references to numerical debugger class.
DEBUG = ddict(NumericalDebug)

@contextmanager
def lineplot(name, with_ax=False, halflife=20, xlabel=None, ylabel=None, title=None, **style):
    with axman(name, xlabel=xlabel, ylabel=ylabel, title=title) as ax:
        data = DATA[name]
        if with_ax:
            yield (data, ax)
        else:
            yield data
        ax.plot(list(range(len(data))), data, alpha=0.5, **style)
        if halflife:
            ax.plot(pd.Series(data).ewm(halflife=halflife).mean(), alpha=0.5, c='k', lw=2)


@contextmanager
def axman(name, xlabel=None, ylabel=None, title=None, clear=True):
    """`axman` is axis manager. Manages clearing, updating and maintaining a global
    handle to a named plot.

    """
    ax = AX[name]
    prev_ax = pl.gca()
    with update_ax(ax, clear=clear):
        _try_sca(ax)
        yield ax
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.set_title(title or name)  # `title` overrides `name`.
        #ax.figure.tight_layout()
        _try_sca(prev_ax)


def _try_sca(ax):
    try:
        pl.sca(ax)
    except ValueError:
        pass


@contextmanager
def update_ax(ax, clear=True):
    "Manages clearing and updating a plot."
    if not hasattr(ax, '_did_show'):
        ax._did_show = False
    if clear:
        ax.clear()
    yield
    for _ in range(2):
        try:
            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events()
            if not ax._did_show:
                pl.show(block=False)
                ax._did_show = True
        except (NotImplementedError, AttributeError):
            #print >> stderr, 'warning failed to update plot.'
            pass


@contextmanager
def scatter_manager(name, with_ax=False, xlabel=None, ylabel=None, title=None, **style):
    with axman(name, xlabel=xlabel, ylabel=ylabel, title=title) as ax:
        data = DATA[name]
        if with_ax:
            yield (data, ax)
        else:
            yield data
        x,y = list(zip(*data))
        ax.scatter(x, y, alpha=0.5, lw=0, **style)


def test():
    d = DEBUG['test1']
    d.update(want=1, have=1)
    d.update(want=1, have=1.01)
    d.update(want=1, have=0.99)
    print(d.df)


if __name__ == '__main__':
    test()
