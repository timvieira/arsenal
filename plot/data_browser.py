import numpy as np
import pylab as P
from matplotlib.text import Annotation

try:
    from debug import ip
except ImportError:
    pass

class PointBrowser(object):
    """
    Click on a point to select and highlight it and trigger callback

    Use the 'n' and 'p' keys to browse through the next and pervious points

    Use arrow keys to scroll along the x-axis

    Use -/+ to zoom along x-axis
    """

    def __init__(self, points, X, xcol, ycol, fig, ax, callback):
        self.index = 0
        self.callback = callback
        self.X = X
        self.xcol = xcol
        self.ycol = ycol
        self.idxs = list(self.X.T)
        self.points = points
        self.ax = ax
        self.fig = fig
        self.text = ax.text(0.01, 0.97, '', transform=ax.transAxes, va='top')
        self.selected = None
        self.update()
        fig.canvas.mpl_connect('pick_event', self.onpick)
        fig.canvas.mpl_connect('key_press_event', self.onpress)

    def select_point(self, x, y):
        if self.selected is None:
            [self.selected] = self.ax.plot([x], [y], 'o', ms=12, alpha=0.4,
                                           color='yellow', visible=False)
        self.selected.set_visible(True)
        self.selected.set_data(x, y)
        self.keep_in_view()

    def onpress(self, event):
        if self.index is None: return
        if event.key in ('=', '+'):
            self.zoom(0.25)
        elif event.key in ('-', '_'):
            self.zoom(1.5)
        elif event.key == 'right':
            self.ax.xaxis.pan(1)
        elif event.key == 'left':
            self.ax.xaxis.pan(-1)
        elif event.key == 'up':
            self.ax.yaxis.pan(+1)
        elif event.key == 'down':
            self.ax.yaxis.pan(-1)
        elif event.key == 'n':
            self.next_point(+1)
        elif event.key == 'p':
            self.next_point(-1)
        elif event.key == 'i':

            idx = self.idxs[self.index]
            picked = self.X.ix[idx]

            l = picked['$item']
            x = picked[self.xcol]
            y = picked[self.ycol]

            # todo: automatic placement of label -- need a way to avoiding collisions
            a = self.ax.annotate(l, xy=(x, y),
                                 xytext=(0, -30), textcoords='offset points',
                                 arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10",
                                                 color='k', alpha=0.5),
                                 fontsize=9, rotation=90, color='k', alpha=0.5)
            a.draggable(use_blit=True)
            
        else:
            return
        self.draw()

    def zoom(self, scale):
        (a,b) = self.ax.get_xlim()
        w = float(b - a)
        mid = a + w/2
        (c,d) = (mid - scale*w, mid + scale*w)
        self.ax.set_xlim(c, d)
        self.keep_in_view()
        self.draw()

    def draw(self):
        self.fig.canvas.draw()

    def keep_in_view(self):
        idx = self.idxs[self.index]
        picked = self.X.ix[idx]
        keep_in_view(self.ax, picked[self.xcol], picked[self.ycol])

    def next_point(self, inc):
        self.index = (self.index + inc) % len(self.idxs)
        self.update()

    def onpick(self, event):
        # filter-out irrelevant events
        if isinstance(event.artist, Annotation): return True
        if event.artist != self.points and event.artist not in self.points: return True
        N = len(event.ind)
        if not N: return True
        # determine click location. there may be more than one point with-in the
        # 5pt tolerance; we'll take the closest
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        distances = np.hypot(x - self.X[self.xcol][event.ind], y - self.X[self.ycol][event.ind])
        idx = distances.argmin()
        self.index = event.ind[idx]
        self.update()

    def update(self):
        i = self.index
        idx = self.idxs[i]
        picked = self.X.ix[idx]
        self.select_point(picked[self.xcol], picked[self.ycol])
        self.callback(self, picked)
        self.draw()


def keep_in_view(ax, x, y, centered=False):
    "Adjust axis limits to keep point (x,y) in view while keeping width the same."

    xmin, xmax = ax.get_xlim()
    w = xmax - xmin
    if centered:
        ax.set_xlim(x - w/2, x + w/2)
        ax.set_xlim(x - w/2, x + w/2)
    else:
        if x < xmin:
            ax.set_xlim(x, x + w)
        if x > xmax:
            ax.set_xlim(x - w, x)

    ymin, ymax = ax.get_ylim()
    w = ymax - ymin
    if y < ymin:
        ax.set_ylim(y, y + w)
    if y > ymax:
        ax.set_ylim(y - w, y)
