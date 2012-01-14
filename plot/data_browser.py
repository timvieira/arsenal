import numpy as np
import pylab as P

class PointBrowser(object):
    """
    Click on a point to select and highlight it -- the data that generated the
    point will be shown in the lower axes.  Use the 'n' and 'p' keys to browse
    through the next and pervious points
    """
    def __init__(self, xs, ys, fig, ax, callback):
        self.index = 0
        self.callback = callback
        self.xs = xs
        self.ys = ys
        self.points, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance

        self.ax = ax
        self.fig = fig

        self.text = ax.text(0.01, 0.97, 'selected: none',
                            transform=ax.transAxes, va='top')

        self.selected = None

        fig.canvas.mpl_connect('pick_event', self.onpick)
        fig.canvas.mpl_connect('key_press_event', self.onpress)


    def select_point(self, x, y):
        if self.selected is None:
            [self.selected] = self.ax.plot([x], [y], 'o', ms=12, alpha=0.4,
                                           color='yellow', visible=False)
        self.selected.set_visible(True)
        self.selected.set_data(x, y)

    def onpress(self, event):
        if self.index is None: return
        if event.key == 'n':
            inc = 1
        elif event.key == 'p':
            inc = -1
        else:
            return
        self.index = (self.index + inc) % len(self.xs)
        self.update()

    def onpick(self, event):
        # filter-out irrelevant events
        if event.artist != self.points: return True
        N = len(event.ind)
        if not N: return True

        # the click locations
        x, y = event.mouseevent.xdata, event.mouseevent.ydata

        # find closest point
        distances = np.hypot(x - self.xs[event.ind], y - self.ys[event.ind])
        self.index = event.ind[distances.argmin()]

        self.update()

    def update(self):
        i = self.index
        self.select_point(self.xs[i], self.ys[i])
        self.callback(self, i)
        self.fig.canvas.draw()

def main():
    X = np.random.rand(100, 200)
    xs = np.mean(X, axis=1)
    ys = np.std(X, axis=1)

    fig = P.figure()
    ax = fig.add_subplot(211)
    ax.set_title('click on point to plot time series')
    ax2 = fig.add_subplot(212)

    def callback(browser, index):

        # clear axis
        ax2.cla()

        # update some text on the selection axis
        browser.text.set_text('selected: %d' % index)

        # plot data
        ax2.plot(X[index])

        # write some text
        ax2.text(0.01, 0.97, 'mu=%1.3f\nsigma=%1.3f' % (xs[index], ys[index]),
                 transform=ax2.transAxes, va='top')

        ax2.set_ylim(-0.5, 1.5)

        ax2.figure.canvas.draw()

    browser = PointBrowser(xs=xs,
                           ys=ys,
                           ax=ax,
                           fig=fig,
                           callback=callback)

    P.show()

if __name__ == '__main__':
    main()
