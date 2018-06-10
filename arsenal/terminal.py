# -*- coding: utf-8 -*-
from __future__ import print_function
import sys


normal = '\x1b[0m%s\x1b[0m'
bold = '\x1b[1m%s\x1b[0m'
italic = "\x1b[3m%s\x1b[0m"
underline = "\x1b[4m%s\x1b[0m"
strike = "\x1b[9m%s\x1b[0m"
#overline = lambda x: (u''.join(unicode(c) + u'\u0305' for c in unicode(x))).encode('utf-8')

leftarrow = '←'
rightarrow = '→'
reset = '\x1b[0m'


def ansi(color=None, light=None, bg=3):
    return '\x1b[%s;%s%sm' % (light, bg, color)


def colorstring(s, c):
    return c + s + reset

class colors:
    black, red, green, yellow, blue, magenta, cyan, white = \
        [colorstring('%s', ansi(c, 0)) for c in range(8)]

    light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = \
        [colorstring('%s', ansi(c, 1)) for c in range(8)]

    dark_black, dark_red, dark_green, dark_yellow, dark_blue, dark_magenta, dark_cyan, dark_white = \
        [colorstring('%s', ansi(c, 2)) for c in range(8)]

    bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = \
        [colorstring('%s', ansi(c, 0, bg=4)) for c in range(8)]


# XXX: Redundant with class above. I did it for backward compatibility
black, red, green, yellow, blue, magenta, cyan, white = \
    [colorstring('%s', ansi(c, 0)) for c in range(8)]

light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = \
    [colorstring('%s', ansi(c, 1)) for c in range(8)]

dark_black, dark_red, dark_green, dark_yellow, dark_blue, dark_magenta, dark_cyan, dark_white = \
    [colorstring('%s', ansi(c, 2)) for c in range(8)]

bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = \
    [colorstring('%s', ansi(c, 0, bg=4)) for c in range(8)]



#def padr(w):
#    "get format to pad right elements"
#    return '%%%ss' % w
#pad = padr
#def padl(w):
#    "get format to pad left elements"
#    return '%%-%ss' % w
#def getwidth(a):
#    "Find maximum width of the string representations of the elements of ``a``."
#    return max(len(str(z)) for z in a)


def check(x, t='pass', f='fail'):
    return green % t if x else red % f


def color01(x, fmt='%.10f', min_color=235, max_color=255):
    "Colorize numbers in [0,1] based on value; darker means smaller value."
    import colored
    if not (0 <= x <= 1 + 1e-10):
        return red % fmt % x
    width = max_color - min_color
    color = min_color + int(round(x*width))
    return '%s%s%s' % (colored.fg(color), (fmt % x), colored.attr('reset'))


def console_width(minimum=None, default=80):
    "Return width of available window area."
    from tqdm._utils import _environ_cols_wrapper
    return max(minimum or 0, _environ_cols_wrapper()(sys.stdout) or default)


def marquee(msg=''):
    return ('{0:*^%s}' % console_width()).format(msg)



def tests():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print('%18s %24s %23s %21s' % (globals()[c] % c,
                                       globals()['light_' + c] % ('light_' + c),
                                       globals()['dark_' + c] % ('dark_' + c),
                                       globals()['bg_' + c] % ('bg_' + c)))

    print(underline % 'underline')
    print(italic % 'italic')
    print(strike % 'strike')

    import numpy as np
    for x in np.linspace(0, 1, 15):
        print(color01(x, fmt='%.2f'))

    print()
    print('Composability')
    print('=============')
    b = ((blue % 'blue %s blue') % (green % 'green'))
    print('normal %s normal' % ((red % 'red %s red %s red') % (b,b)))

    b = ((blue % 'blue {0} blue').format(green % 'green'))
    print('normal {middle} normal'.format(middle = ((red % 'red %s red %s red') % (b,b))))

    w = console_width()
    print('Console width:', w, sep=' ')
    print('='*w)
    print(marquee(' marquee '))


if __name__ == '__main__':
    tests()
