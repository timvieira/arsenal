# -*- coding: utf-8 -*-
import re, os, sys
from glob import glob
from subprocess import Popen, PIPE


def ansi2html(x):
    p = Popen('ansi2html.sh', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.stdin.write(str(x).encode('utf-8'))
    return p.communicate()[0].decode('utf-8')


def link(url, text=None):
    if text is None:
        text = url
    return f"\033]8;;{url}\a{text}\033]8;;\a"


def overline(xs):
    return ''.join(f'{x}\u0305' for x in xs)


partial = '∂'

visible_space = '␣'

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

class arrow:
    u = up = '↑'
    ur = '↗'
    r = right = '→'
    dr = '↘'
    dl = '↙'
    d = down = '↓'
    l = left =  '←'
    ul = '↖'

    class long:
        right = r = '⟶'
        leftright = lr = '⟷'
        left = l = '⟵'

    class Long:
        leftright = lr = '⟺'
        left = l = '⟸'
        right = r = '⟹'

    class squiggle:
        right = r = '⟿'


arrows = arrow.__dict__

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

    def rgb(r,g,b):
        return f"\x1b[48;2;{r};{g};{b}m%s\x1b[0m"

    orange = rgb(255, 165, 0)
    rgb = staticmethod(rgb)

def rgb(r,g,b):
    return f"\x1b[38;2;{r};{g};{b}m%s\x1b[0m"

orange = rgb(255, 165, 0)

purple = '\x1b[38;5;91m' + '%s' + _reset


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


def nocolor(x):
    "Remove ANSI control codes from the given string `x`."
    return re.sub(r'\033\[[0-9;]*m', "", x)


# https://www.w3.org/TR/xml-entity-names/025.html
def branch(xs):
    ys = []
    for i, x in enumerate(xs):
        first = i == 0
        last = i == len(xs)-1
        if last and first:
            h = '└─'
        elif last:
            h = '└─'
        elif first:
            h = '┌─' #'├─'
        else:
            h = '├─'
        if not x:
            continue
        ys.append(h + x[0])
        indent = '│ ' if not last else '  '
        for a in x[1:]:
            ys.append(indent + a)
    return ys


def line(n): return '─'*(n)

def thick_line(n): return ('━'*80)

def mark_(x): return '✔' if x else '✘'

def faster(x, y, color=True):
    "is x faster than y"
    msg = f'{x / y:.2f}x faster' if x > y else f'{y / x:.2f}x slower'
    msg = f'{msg} ({x:g} s vs {y:g} s)'
    if color: msg = (green if x > y else yellow) % msg
    return msg

from textwrap import dedent

def indent(indentation, msg):
    if isinstance(msg, str): msg = msg.split('\n')
    return '\n'.join(indentation + line for line in msg)


def reindent(indentation, msg):
    return indent(indentation, dedent(msg))

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


def render(y, **kwargs):
    """
    Render colorful string using 'reset' to mean 'pop the color stack' rather than
    go directly 'normal' color.
    """
    return rendering(y, **kwargs).value


class rendering:
    def __init__(self, y, debug=False):
        y = str(y)
        xs = re.split(r'(\x1b\[[0-9;]+m)', y)  # tokenize.

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
        [(pad, fmt)] = re.findall(r'^(-?\d*)(s)$', spec)
        pad = int(pad)
        if pad > 0:
            return self.value + ' '*max(0, pad - len(self))
        else:
            return ' '*max(0, abs(pad) - len(self)) + self.value


ok   = green     % 'ok'
warn = yellow    % 'warn'
fail = light.red % 'fail'
bad  = light.red % 'bad'
error  = light.red % 'error'


thumbs_up = '👍'
thumbs_down = '👎'
poop = poo = turd = '💩'
timeout = '⌛'

trophy = '🏆'

lightbulb = '💡'
fire = '🔥'
lightning = '⚡'

#lightning = '⚡'
#lightning = '↯'
#lightning = 'ϟ'

check = green % '✔' #'✓'
xmark = dark.red % '✘' # ☒ - Unicode Character Table
def mark(x): return check if x else xmark

def percent(num, den):
    if den == 0:
        return f'{100:.1f}% (0/0)'
    return f'{num*100/den:.1f}% ({num}/{den})'
percentage = percent


