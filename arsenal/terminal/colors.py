# -*- coding: utf-8 -*-

# TODO: Consider using the "fabulous" package for most of this. It supports a
# wider variety of colors and might do a better job with Macs.

normal = '\x1b[0m%s\x1b[0m'
bold = '\x1b[1m%s\x1b[0m'
italic = "\x1b[3m%s\x1b[0m"
underline = "\x1b[4m%s\x1b[0m"
strike = "\x1b[9m%s\x1b[0m"
#overline = lambda x: (u''.join(unicode(c) + u'\u0305' for c in unicode(x))).encode('utf-8')

leftarrow = '←'
rightarrow = '→'

def ansi(color=None, light=None, bg=3):
    return '\x1b[%s;%s%sm' % (light, bg, color)

reset = '\x1b[0m'

#class colorstring(unicode):
#
#    def __new__(cls, x, l, r=reset):
#        l = l
#        s = l + x + r
#
#        # TODO: could just try to infer the right way to pop the color stack.
#        #import re
#        #controls = re.findall('(\x1b\[.+?m)', l + x + r)
#
#        self = unicode.__new__(colorstring, s)
#        self.x = x
#        self.l = l
#        self.r = r
#
#        return self
#
#    def __repr__(self):
#        #return 'colorstring%s' % repr((self.l, self.x, self.r))
#        return str(self)
#
#    def __call__(self, x):
#        return self % x
#
#    def __mod__(self, x):
#        if not isinstance(x, tuple):
#            x = (x,)
#        y = tuple(map(self._inhert_right, x))
#        return colorstring(self.x % tuple(y), l=self.l, r=self.r)
#
#    def format(self, *args, **kw):
#        args = tuple(map(self._inhert_right, args))
#        kw = {k: self._inhert_right(v) for k, v in kw.items()}
#        return colorstring(self.x.format(*args, **kw), l=self.l, r=self.r)
#
#    def _inhert_right(self, x):
#        if isinstance(x, colorstring):
#            return colorstring(x.x, l=x.l, r=self.l)   # take right formatter from self
#        else:
#            return x

def colorstring(s, c):
    return c + s + reset


black, red, green, yellow, blue, magenta, cyan, white = \
    [colorstring('%s', ansi(c, 0)) for c in range(8)]

light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = \
    [colorstring('%s', ansi(c, 1)) for c in range(8)]

dark_black, dark_red, dark_green, dark_yellow, dark_blue, dark_magenta, dark_cyan, dark_white = \
    [colorstring('%s', ansi(c, 2)) for c in range(8)]

bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = \
    [colorstring('%s', ansi(c, 0, bg=4)) for c in range(8)]


def padr(w):
    "get format to pad right elements"
    return '%%%ss' % w

pad = padr

def padl(w):
    "get format to pad left elements"
    return '%%-%ss' % w

def getwidth(a):
    "Find maximum width of the string representations of the elements of ``a``."
    return max(len(str(z)) for z in a)

def check(x, t='pass', f='fail'):
    return green % t if x else red % f


def test():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print '%18s %24s %23s %21s' % (globals()[c] % c,
                                       globals()['light_' + c] % ('light_' + c),
                                       globals()['dark_' + c] % ('dark_' + c),
                                       globals()['bg_' + c] % ('bg_' + c))

    print underline % 'underline'
    print italic % 'italic'
    print strike % 'strike'

    print
    print 'Composability'
    print '============='
    b = ((blue % 'blue %s blue') % (green % 'green'))
    print 'normal %s normal' % ((red % 'red %s red %s red') % (b,b))

    b = ((blue % 'blue {0} blue').format(green % 'green'))
    print 'normal {middle} normal'.format(middle = ((red % 'red %s red %s red') % (b,b)))

    # TODO: this example doesn't work :-(
    print (green % 'green %s green') % {red % 'red': blue % 'blue'}


# TODO: needs some work, but it's pretty fun to use
def color01(x, fmt='%.10f', min_color=235, max_color=255):
    "Colorize numbers in [0,1] based on value; darker means smaller value."
    import colored
    if not (0 <= x <= 1 + 1e-10):
        return red % fmt % x
    width = max_color - min_color
    color = min_color + int(round(x*width))
    return '%s%s%s' % (colored.fg(color), (fmt % x), colored.attr('reset'))


if __name__ == '__main__':
    test()
