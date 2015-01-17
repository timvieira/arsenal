# coding=utf-8
"""
Hinton diagrams for the terminal

original version:
https://github.com/shawntan/theano_toolkit/blob/master/hinton.py

with a few changes by Tim Vieira
"""

from __future__ import division


import numpy as np

chars = [" ","▁","▂","▃","▄","▅","▆","▇"] #"█"]

def plot(arr, max_arr=None):
    if max_arr is None:
        max_arr = arr
    max_val = max(abs(np.max(max_arr)),abs(np.min(max_arr)))
    print np.array2string(arr,
                          formatter={'float_kind': lambda x: visual(x,max_val)},
                          max_line_width = 5000)

def visual(val, max_val):
    if abs(val) == max_val:
        step = len(chars)-1
    else:
        step = int(abs(val/max_val)*len(chars))
    if val < 0:
        return '\033[90m%s\033[0m' % chars[step]
    else:
        return chars[step]

if __name__ == "__main__":
    plot(np.random.randn(10,10))
