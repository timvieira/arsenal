from numpy.random import rand
from numpy import arange
import pylab

def labeled_points():
    N = 15
    y = rand(N)
    t = rand(N)
    label = ['label%d' % i for i in xrange(N)]
    for i in range(N):
        pylab.plot([t[i]], [y[i]], 'o')
        pylab.text(t[i], y[i], label[i], fontsize=8, rotation=30, color='green')
    pylab.grid()
    pylab.show()

if __name__ == '__main__':
    labeled_points()
