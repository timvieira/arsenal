from os import environ
DISPLAY = True
if not environ.get('DISPLAY'):
    import matplotlib
    #print 'Not a display environment.'
    matplotlib.use('Agg')
    DISPLAY = False

from pandas import ewma
import pylab as pl
import numpy as np
from sys import stderr
from collections import defaultdict
from contextlib import contextmanager
from matplotlib.backends.backend_pdf import PdfPages
from arsenal.terminal import yellow
from arsenal.viz.covariance_ellipse import covariance_ellipse


def save_plots(pdf):
    "save all plots to pdf"
    pp = PdfPages(pdf)
    for i in pl.get_fignums():
        pl.figure(i)
        pl.savefig(pp, format='pdf')
    pp.close()
    print yellow % 'saved plots to "%s"' % pdf


# global reference to all of the plots
def newax():
    return pl.figure().add_subplot(111)
AX = defaultdict(newax)
DATA = defaultdict(list)


@contextmanager
def lineplot(name, with_ax=False, halflife=20, xlabel=None, ylabel=None, title=None, **style):
    with axman(name, xlabel=xlabel, ylabel=ylabel, title=title) as ax:
        data = DATA[name]
        if with_ax:
            yield (data, ax)
        else:
            yield data
        ax.plot(range(len(data)), data, alpha=0.5, **style)
        if halflife:
            ax.plot(ewma(np.asarray(data), halflife=halflife), alpha=0.5, c='k', lw=2)


@contextmanager
def axman(name, xlabel=None, ylabel=None, title=None, clear=True):
    """`axman` is axis manager. Manages clearing, updating and maintaining a global
    handle to a named plot.

    """
    ax = AX[name]
    prev_ax = pl.gca()
    with update_ax(ax, clear=clear):
        pl.sca(ax)
        yield ax
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.set_title(title or name)  # `title` overrides `name`.
        #ax.figure.tight_layout()
        pl.sca(prev_ax)


@contextmanager
def update_ax(ax, clear=True):
    "Manages clearing and updating a plot."
    if clear:
        ax.clear()
    yield
    try:
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()
        pl.show(block=False)
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
        x,y = zip(*data)
        ax.scatter(x, y, alpha=0.5, lw=0, **style)
