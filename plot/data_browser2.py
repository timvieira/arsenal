from pylab import *
import sys

from numpy import *
class PointBrowser:


    def __init__(self,xs,ys):

        self.xs = array(xs)
        self.ys = array(ys)

        self.fig = figure()
        self.ax = self.fig.add_subplot(111)

        self.line, = self.ax.plot(self.xs,self.ys,'ro ', picker=5)

        self.lastind = 0

        self.text = self.ax.text(0.05, 0.95, 'Datapoint index selected: none',
                            transform=self.ax.transAxes, va='top')

        self.selected,  = self.ax.plot([self.xs[0]],
                                       [self.ys[0]], 'o', ms=12, alpha=0.4,
                                       color='yellow', visible=False)


        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)



    def onpress(self, event):
        'define some key press events'
        if self.lastind is None: return

        if event.key in ('q','Q'): sys.exit()

        if event.key not in ('n', 'p'): return
        if event.key=='n': inc = 1
        else:  inc = -1


        self.lastind += inc
        self.lastind = clip(self.lastind, 0, len(self.xs)-1)
        self.update()

    def onpick(self, event):

        if event.artist!=self.line: return True

        N = len(event.ind)
        if not N: return True

        if N > 1:
            print '%i points found!' % N


        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        dx = array(x-self.xs[event.ind],dtype=float)
        dy = array(y-self.ys[event.ind],dtype=float)

        distances = hypot(dx,dy)
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None: return

        dataind = self.lastind

        self.selected.set_visible(True)
        self.selected.set_data(self.xs[dataind], self.ys[dataind])

        self.text.set_text('datapoint index selected: %d'%dataind)

        # put a user function in here!        
        self.userfunc(dataind)

        self.fig.canvas.draw()


    def userfunc(self,dataind):
        print 'No userfunc defined'
        pass



if __name__ == '__main__':
    import numpy as npy
    from pylab import *


    X = npy.random.rand(100, 200)
    xs = npy.mean(X, axis=1)
    ys = npy.std(X, axis=1)


    p = PointBrowser(xs,ys)

    def plot2(dataind):
        fig2 = figure(2)
        ax2 = fig2.add_subplot(111)

        ax2.cla()
        ax2.plot(X[dataind])

        ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[dataind], ys[dataind]),
                 transform=ax2.transAxes, va='top')
        ax2.set_ylim(-0.5, 1.5)

        fig2.canvas.draw()
        fig2.show()

    p.userfunc = plot2

    xlabel('$\mu$')
    ylabel('$\sigma$')


    show()
