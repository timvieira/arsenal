
"""
Simple demo for selecting lines using matplotlib.
Click on a line to make it think.
"""

import matplotlib.pyplot as plt
import numpy as np

from debug import ip


class LinePicker(object):

    def __init__(self, lines, title=None, tol=4):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        if title:
            ax.set_title(title)

        self.names = []
        self.handles = []  # handles to avoid garbage collection
        for name, x, y in lines:
            [h] = ax.plot(x, y, '-', picker=tol, label=name)
            self.handles.append(h)
            self.names.append(name)

        fig.canvas.mpl_connect('pick_event', self.onpick)

        self.lastartist = self.handles[-1]

    def onpick(self, event):
        self.lastartist.set_linewidth(1)  # reset linewidth of old selection
        self.lastartist = thisline = event.artist
        thisline.set_linewidth(3)
        plt.draw()
        # find the artist for this line
        idx = self.handles.index(event.artist)
        if idx != -1:
            name = self.names[idx]
            print 'selected line:', name


def demo():
    x = np.linspace(0,np.pi,100)
    y1 = np.cos(x)
    y2 = np.sin(x)
    y3 = y1 + np.random.uniform(-0.5, 0.5, size=100)

    picker = LinePicker([('first', x, y1), ('second', x, y2), ('third', x, y3)])

    plt.show()


if __name__ == '__main__':
    demo()
