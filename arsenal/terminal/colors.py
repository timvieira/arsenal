try:
    from fabulous import color
except ImportError:
    pass

# TODO: Consider using fabulous for most of this. It supports a wider variety of
# colors and might do a better job with other macs.

normal = '\033[0m%s\033[0m'
bold = '\033[1m%s\033[0m'

black, red, green, yellow, blue, magenta, cyan, white = \
    map('\033[3%sm%%s\033[0m'.__mod__, range(8))

light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = \
    map('\033[1;3%sm%%s\033[0m'.__mod__, range(8))

bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = \
    map('\033[4%sm%%s\033[0m'.__mod__, range(8))

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

underline = '\033[4m%s\033[0m'

def test():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print globals()[c] % c
        print globals()['light_' + c] % ('light_' + c)

    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print globals()['bg_' + c] % c

    print underline % 'underline'


# TODO: needs some work, but it's pretty fun to use
def color01(x, fmt='%.10f'):
    "Colorize numbers in [0,1] based on value; darker means smaller value."
    if not (0 <= x <= 1 + 1e-10):
        return red % fmt % x
    a, b = 238, 255   # 232, 255
    w = b - a
    offset = x*w
    offset = int(round(offset))
    return color.fg256(a + offset, fmt % x)


if __name__ == '__main__':
    test()
