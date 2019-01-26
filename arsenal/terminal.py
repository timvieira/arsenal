# -*- coding: utf-8 -*-
import sys, os
from glob import glob


def complete_filenames(text, line, begidx, endidx):
    "Util for filename completion."

    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
        return # arg not found

    fixed = line[before_arg+1:begidx]  # fixed portion of the arg

    completions = []
    for p in glob(line[before_arg+1:endidx] + '*'):
        p = p + (os.sep if p and os.path.isdir(p) and p[-1] != os.sep else '')
        completions.append(p.replace(fixed, "", 1))
    return completions


def ansi(color=None, light=None, bg=3):
    return '\x1b[%s;%s%sm' % (light, bg, color)

_reset = '\x1b[0m'

def colorstring(s, c):
    return c + s + _reset


class colors:
    black, red, green, yellow, blue, magenta, cyan, white = \
        [colorstring('%s', ansi(c, 0)) for c in range(8)]

    class light:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 1)) for c in range(8)]

    class dark:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 2)) for c in range(8)]

    class bg:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 0, bg=4)) for c in range(8)]

    normal = '\x1b[0m%s\x1b[0m'
    bold = '\x1b[1m%s\x1b[0m'
    italic = "\x1b[3m%s\x1b[0m"
    underline = "\x1b[4m%s\x1b[0m"
    strike = "\x1b[9m%s\x1b[0m"
    #overline = lambda x: (u''.join(unicode(c) + u'\u0305' for c in unicode(x))).encode('utf-8')

    leftarrow = '←'
    rightarrow = '→'
    reset = _reset


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
    return colors.green % t if x else colors.red % f


def color01(x, fmt='%.10f', min_color=235, max_color=255):
    "Colorize numbers in [0,1] based on value; darker means smaller value."
    import colored
    if not (0 <= x <= 1 + 1e-10):
        return colors.red % fmt % x
    width = max_color - min_color
    color = min_color + int(round(x*width))
    return '%s%s%s' % (colored.fg(color), (fmt % x), colored.attr('reset'))


def console_width(minimum=None, default=80):
    "Return width of available window area."
    from tqdm._utils import _environ_cols_wrapper
    return max(minimum or 0, _environ_cols_wrapper()(sys.stdout) or default)


def marquee(msg=''):
    return ('{0:*^%s}' % console_width()).format(msg)


import re
def render(y, debug=False):
    """
    Render colorful string using 'reset' to mean 'pop the color stack' rather than
    go directly 'normal' color.
    """
    xs = re.split('(\x1b\[[0-9;]+m)', y)  # tokenize.
    s = [_reset]      # stack
    b = []            # buffer
    prefix = '\x1b['  # control code prefix
    c = _reset        # current color
    for x in xs:
        if debug: print('[render] current token', repr(x))
        if x.startswith(prefix):
            if debug: print('[render]   ^ control code')
            if x == _reset:
                c = s.pop() if len(s) else _reset
            else:
                s.append(c)
                c = x
            continue
        else:
            if debug: print('[render]   ^ use color', repr(c))
            b.append(c)
            b.append(x)
    b.append(_reset)   # always end on reset.
    return ''.join(b)


def tests():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print('%18s %24s %23s %21s' % (getattr(colors, c) % c,
                                       getattr(colors.light, c) % f'light.{c}',
                                       getattr(colors.dark, c) % f'dark.{c}',
                                       getattr(colors.bg, c) % f'bg.{c}'))

    print(colors.underline % 'underline')
    print(colors.italic % 'italic')
    print(colors.strike % 'strike')

    import numpy as np
    for x in np.linspace(0, 1, 15):
        print(color01(x, fmt='%.2f'), end=' ')
    print()

    w = console_width()
    print('Console width:', w, sep=' ')
    print('='*w)
    print(marquee(' marquee '))


    print()
    print('Stack-based rendering')
    print('=====================')
    g = colors.green % 'green'
    b = colors.blue % f'blue {g} blue'
    r = colors.red % f'red {b} red {b} red'
    x = colors.normal % f'normal {r} normal'
    print(render(x))



if __name__ == '__main__':
    tests()
