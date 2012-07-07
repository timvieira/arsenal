"""

TODO:

 - sometimes we accidently activate some strange thing from "matplotlib's
   interative toolbar"(e.g. the grabber hand to move things), disabling the
   cursor, which means that we can't click on points... this is annoying.

 - I'd like better arrow-key exploration of point clouds. Priniciple of least
   surprise. I don't believe this is a trivial problem (with out something crazy
   like eye tracking software).

   Things which seem relevant.
    * proximity to current selection
    * history of previous points
    * all points ought to be reachable (no cycles)

"""

import numpy as np
import pylab as pl

# development utils
try:
    from debug import ip
except ImportError:
    pass
#from matplotlib.text import Annotation

def print_row(browser, row):
    print row

class PointBrowser(object):
    """
    Click on a point to select and highlight it and trigger callback

    Use the 'n' and 'p' keys to browse through the next and previous points

    Use arrow keys to scroll along the x-axis

    Use -/+ to zoom along x-axis
    """

    def __init__(self, X, xcol='x', ycol='y', callback=print_row,
                 ax=None, plot=None):
        self.index = 0
        self.callback = callback
        self.X = X
        self.xcol = xcol
        self.ycol = ycol
        self.idxs = list(self.X.T)
        self.selected_row = None

        if plot is not None:
            ax = plot.get_axes()

        if ax is None:
            ax = pl.subplot(111)

        if plot is None:
            plot = ax.scatter(X[xcol], X[ycol])
            ax.grid(True)
            ax.set_xlabel(xcol)
            ax.set_ylabel(ycol)

        # make sure picker is enabled
        if not plot.get_picker():
            plot.set_picker(5)

        self.fig = ax.get_figure()
        self.ax = ax
        self.plot = plot

        self.text = ax.text(0.01, 0.97, '', transform=ax.transAxes, va='top')
        self.selected = None   # tracks selected point

        # register event handlers
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)

    def select_point(self, x, y):
        # TODO: might want to use a cursor (hline and vline) because it's easier
        #   to find point
        if self.selected is None:
            [self.selected] = self.ax.plot([x], [y], 'o', ms=12, alpha=0.4,
                                           color='yellow', visible=False)
        self.selected.set_visible(True)
        self.selected.set_data(x, y)
        keep_in_view(self.ax, x, y)

    def onpress(self, event):
        if self.index is None:     # nothing happend
            return
        elif event.key == 'right':
            self.ax.xaxis.pan(+0.2)
        elif event.key == 'left':
            self.ax.xaxis.pan(-0.2)
        elif event.key == 'up':
            self.ax.yaxis.pan(+0.2)
        elif event.key == 'down':
            self.ax.yaxis.pan(-0.2)

#------------------------------------------------------------------------------
# TODO: zooming is busted. This should be an easy fix.
#------------------------------------------------------------------------------
#        elif event.key in ('=', '+'):
#            self.zoom(0.01)
#        elif event.key in ('-', '_'):
#            self.zoom(1.01)
#------------------------------------------------------------------------------

        elif event.key == 'n':   # move to next point
            self.next_point(+1)
        elif event.key == 'p':
            self.next_point(-1)  # move to previous point

#------------------------------------------------------------------------------
# TODO: adding annotations (labels) works, but isn't ideal because labels are
#    not placed intelligently (just a fixed offset from point). This more often
#    than not occludes other labels or data. A possible solutions is to do some
#    local search (similar to graph layout algorithm). It would also be nice of
#    annotation were draggable.
#------------------------------------------------------------------------------
# TODO: matplotlib's draggable annotations have the following quirk. When
#   panning, labels don't move along with the axes like you might expect them to
#   they keep the same absolute position on the screen even though they should
#   have moved along with the point.
#------------------------------------------------------------------------------
#        elif event.key == 'i' and self.labelcol:
#            idx = self.idxs[self.index]
#            picked = self.X.ix[idx]
#            l = picked[self.labelcol]
#            x = picked[self.xcol]
#            y = picked[self.ycol]
#            a = self.ax.annotate(l, xy=(x, y),
#                                 xytext=(0, -30), textcoords='offset points',
#                                 arrowprops=dict(arrowstyle="->",
#                                 connectionstyle="angle,angleA=0,angleB=90,rad=10",
#                                                 color='k', alpha=0.5),
#                                 fontsize=9, rotation=90, color='k', alpha=0.5)
#            a.draggable(use_blit=True)
#------------------------------------------------------------------------------

        self.draw()

#    def zoom(self, scale):
#        (a,b) = self.ax.get_xlim()
#        w = float(b - a)
#        mid = a + w/2
#        self.ax.set_xlim(mid - scale*w, mid + scale*w)
#        self.draw()

    def draw(self):
        self.fig.canvas.draw()

    def next_point(self, inc):
        self.index = (self.index + inc) % len(self.idxs)
        self.update()

    def onpick(self, event):
        # filter-out irrelevant events
        #if isinstance(event.artist, Annotation): return True
        if event.artist != self.plot and event.artist not in self.plot: return True
        N = len(event.ind)
        if not N: return True   # no points within tolerance
        # click location
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        # There may be more than one point with-in the specified tolerance;
        # we'll take the closest of those point (using Euclidean distance).
        X = self.X[self.xcol][event.ind]
        Y = self.X[self.ycol][event.ind]
        distances = np.hypot(x - X, y - Y)  # distance to pts within tolerance
        idx = distances.argmin()
        self.index = event.ind[idx]
        self.update()

    def update(self):
        i = self.index
        idx = self.idxs[i]
        picked = self.selected_row = self.X.ix[idx]
        self.select_point(picked[self.xcol], picked[self.ycol])
        self.callback(picked)
        self.draw()


def keep_in_view(ax, x, y, **kwargs):
    """
    Adjust axis limits (i.e. pan) to keep point (x,y) in view while keeping
    width the same. Same options as adjust_axis.
    """
    adjust_axis(ax, 'x', x, **kwargs)
    adjust_axis(ax, 'y', y, **kwargs)


def adjust_axis(ax, dim, x, centered=False, margin=0.1):
    """
    Adjust axis, ``ax`` along dimension ``dim``. The value ``x`` is a point
    along that axis which is the reference point for the adjustment.
    """
    if dim == 'x':
        get_lim, set_lim = (ax.get_xlim, ax.set_xlim)
    elif dim == 'y':
        get_lim, set_lim = (ax.get_ylim, ax.set_ylim)
    else:
        raise NotImplementedError('Dimension %s not supported' % dim)
    if centered: margin = 0.5
    xmin, xmax = get_lim()
    w = xmax - xmin           # width of axis along dim
    margin = margin * w       # convert from percentage to size
    if x - margin < xmin:
        # shift left by margin; keep same width
        set_lim(x - margin, x - margin + w)
    if x + margin > xmax:
        set_lim(x + margin - w, x + margin)


def main():
    import pandas
    from numpy.random import uniform

    n = 25
    m = pandas.DataFrame({'x': uniform(-1, 1, size=n),
                          'y': uniform(-1, 1, size=n),
                          'size': uniform(3, 10, size=n) ** 2,
                          'color': uniform(0, 1, size=n)})

    # payload some random information we'd like to plot in the other subplot.
    payload_domain = np.arange(0, 10, 0.1)
    m['payload'] = [a*np.sin(payload_domain) for a in m['x']]

    def callback(row):
        print
        print row
        ax2.clear()
        ax2.plot(payload_domain, row['payload'])

    ax1 = pl.subplot(211)
    ax2 = pl.subplot(212)

    #plot = None
    plot = ax1.scatter(m['x'], m['y'], c=m['color'], s=m['size'])
    #[plot] = ax1.plot(m['x'], m['y'], lw=2,
    #                  marker='o', markersize=5, markerfacecolor='b',
    #                  linewidth=0.5, c='r')

    b = PointBrowser(m, callback=callback, ax=ax1, plot=plot)
    pl.show()


if __name__ == '__main__':
    main()
