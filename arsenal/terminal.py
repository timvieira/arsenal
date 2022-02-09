# -*- coding: utf-8 -*-
import sys, os
from glob import glob
from subprocess import Popen, PIPE


def ansi2html(x):
    p = Popen('ansi2html.sh', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.stdin.write(str(x).encode('utf-8'))
    return p.communicate()[0].decode('utf-8')


def overline(xs):
    return ''.join(f'{x}\u0305' for x in xs)


partial = '∂'


class bb:
    A = '𝔸'
    B = '𝔹'
    C = 'ℂ'
    D = '𝔻'
    E = '𝔼'
    F = '𝔽'
    G = '𝔾'
    H = 'ℍ'
    I = '𝕀'
    J = '𝕁'
    K = '𝕂'
    L = '𝕃'
    M = '𝕄'
    N = 'ℕ'
    O = '𝕆'
    P = 'ℙ'
    Q = 'ℚ'
    R = 'ℝ'
    S = '𝕊'
    T = '𝕋'
    U = '𝕌'
    V = '𝕍'
    W = '𝕎'
    X = '𝕏'
    Y = '𝕐'
    Z = 'ℤ'


# https://stackoverflow.com/questions/8651361/how-do-you-print-superscript-in-python
superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹",
    0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶",
    7: "⁷", 8: "⁸", 9: "⁹",
    "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾",
}

subscript_map = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
    "7": "₇", "8": "₈", "9": "₉",
    0: "₀", 1: "₁", 2: "₂", 3: "₃", 4: "₄", 5: "₅", 6: "₆",
    7: "₇", 8: "₈", 9: "₉",
    "a": "ₐ", "b": "♭", "c": "꜀", "d": "ᑯ",
    "e": "ₑ", "f": "բ", "g": "₉", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ",
    "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "q": "૧", "r": "ᵣ",
    "s": "ₛ", "t": "ₜ", "u": "ᵤ", "v": "ᵥ", "w": "w", "x": "ₓ", "y": "ᵧ",
    "z": "₂", "A": "ₐ", "B": "₈", "C": "C", "D": "D", "E": "ₑ", "F": "բ",
    "G": "G", "H": "ₕ", "I": "ᵢ", "J": "ⱼ", "K": "ₖ", "L": "ₗ", "M": "ₘ",
    "N": "ₙ", "O": "ₒ", "P": "ₚ", "Q": "Q", "R": "ᵣ", "S": "ₛ", "T": "ₜ",
    "U": "ᵤ", "V": "ᵥ", "W": "w", "X": "ₓ", "Y": "ᵧ", "Z": "Z", "+": "₊",
    "-": "₋", "=": "₌", "(": "₍", ")": "₎",
}

arrows = {
    'u':  '↑',
    'ur': '↗',
    'r':  '→',
    'dr': '↘',
    'd':  '↓',
    'dl': '↙',
    'l':  '←',
    'ul': '↖',
}

def superscript(x):
    return "".join(superscript_map[i] for i in str(x))

def subscript(x):
    return "".join(subscript_map[i] for i in str(x))


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

    ansi2html = ansi2html

    @staticmethod
    def line(n):
        return '─'*(n)


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


#def color01(x, fmt='%.10f', min_color=235, max_color=255):
#    "Colorize numbers in [0,1] based on value; darker means smaller value."
#    import colored
#    if not (0 <= x <= 1 + 1e-10):
#        return colors.red % fmt % x
#    width = max_color - min_color
#    color = min_color + int(round(x*width))
#    return '%s%s%s' % (colored.fg(color), (fmt % x), colored.attr('reset'))


def console_width(minimum=None, default=80):
    "Return width of available window area."
    from tqdm.utils import _screen_shape_wrapper
    x = _screen_shape_wrapper()(sys.stdout)[0]
    return max(minimum or 0, x or default)


def marquee(msg=''):
    return ('{0:*^%s}' % console_width()).format(msg)


import re
def render(y, **kwargs):
    """
    Render colorful string using 'reset' to mean 'pop the color stack' rather than
    go directly 'normal' color.
    """
    return rendering(y, **kwargs).value


class rendering:
    def __init__(self, y, debug=False):
        y = str(y)
        xs = re.split('(\x1b\[[0-9;]+m)', y)  # tokenize.

        if debug:
            msg = lambda *args: print(f'[render]{"    "*len(s)}', *args)

        s = [_reset]      # stack
        b = []            # buffer
        prefix = '\x1b['  # control code prefix
        c = _reset        # current color
        for x in xs:
            if debug: msg('current token', repr(x))
            if x.startswith(prefix):
                if x == _reset:
                    if debug: msg('   ^ pop')
                    c = s.pop() if len(s) else _reset
                else:
                    if debug: msg('   ^ control code', x + repr(x) + _reset)
                    s.append(c)
                    c = x
                continue
            else:
                if debug: msg('   ^ color', c + repr(x) + _reset)
                b.append(c)
                b.append(x + _reset)
        b.append(_reset)   # always end on reset.
        self.xs = xs
        self.value = ''.join(b)

    def __len__(self):
        return sum(len(x) for x in self.xs if not x.startswith('\x1b['))  # control code prefix

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __format__(self, spec):
        [(pad, fmt)] = re.findall('^(-?\d*)(s)$', spec)
        pad = int(pad)
        if pad > 0:
            return self.value + ' '*max(0, pad - len(self))
        else:
            return ' '*max(0, abs(pad) - len(self)) + self.value



colors.render = render
colors.rendering = rendering


ok   = colors.green     % 'ok'
warn = colors.yellow    % 'warn'
fail = colors.light.red % 'fail'
bad  = colors.light.red % 'bad'
error  = colors.light.red % 'error'


thumbs_up = '👍'
thumbs_down = '👎'
poop = poo = turd = '💩'
timeout = '⌛'


colors.poop = poop
colors.ok = ok
colors.warn = warn
colors.fail = fail
colors.bad = bad
colors.timeout = timeout


def tests():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print('%18s %24s %23s %21s' % (getattr(colors, c) % c,
                                       getattr(colors.light, c) % f'light.{c}',
                                       getattr(colors.dark, c) % f'dark.{c}',
                                       getattr(colors.bg, c) % f'bg.{c}'))

    print(colors.underline % 'underline')
    print(colors.italic % 'italic')
    print(colors.strike % 'strike')

    #import numpy as np
    #for x in np.linspace(0, 1, 15):
    #    print(color01(x, fmt='%.2f'), end=' ')
    #print()

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

    # SDD: make sure we reset after dark
    print(render(
        (colors.light.blue % 'light %s light'
         % colors.dark.blue % 'dark %s dark'
         % colors.blue % 'regular'),
        #debug = True,
    ))

    print(thumbs_up, thumbs_down)


if __name__ == '__main__':
    tests()
