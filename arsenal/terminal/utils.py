import os, sys

try:
    import readline
except ImportError:
    pass

def substring_completer(values, normalize=lambda x: x.lower()):
    completions = {}
    values = [(v, normalize(v)) for v in values]

    def completer(text, state):
        try:
            matches = completions[text]   # timv: caching (maybe we don't want to do this.. maybe use an LRU)
        except KeyError:
            matches = [v for v, normalized_v in values if normalize(text) in normalized_v]
            completions[text] = matches
        try:
            return matches[state]
        except IndexError:
            return None

    readline.set_completer(completer)
    readline.parse_and_bind('tab: menu-complete')


def console_width(minimum=None, default=80):
    """Return width of available window area. Autodetection works for
    Windows and POSIX platforms. Returns 80 for others

    Code based on http://bitbucket.org/techtonik/python-pager
    """
    if os.name == 'nt':
        STD_INPUT_HANDLE  = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE  = -12

        # get console handle
        from ctypes import windll, Structure, byref
        from ctypes.wintypes import SHORT, WORD, DWORD
        console_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        # CONSOLE_SCREEN_BUFFER_INFO Structure
        class COORD(Structure):
            _fields_ = [("X", SHORT), ("Y", SHORT)]

        class SMALL_RECT(Structure):
            _fields_ = [("Left", SHORT), ("Top", SHORT),
                        ("Right", SHORT), ("Bottom", SHORT)]

        class CONSOLE_SCREEN_BUFFER_INFO(Structure):
            _fields_ = [("dwSize", COORD),
                        ("dwCursorPosition", COORD),
                        ("wAttributes", WORD),
                        ("srWindow", SMALL_RECT),
                        ("dwMaximumWindowSize", DWORD)]

        sbi = CONSOLE_SCREEN_BUFFER_INFO()
        ret = windll.kernel32.GetConsoleScreenBufferInfo(console_handle, byref(sbi))
        if ret == 0:
            return max(minimum, 0)
        return max(minimum, sbi.srWindow.Right+1)

    elif os.name == 'posix':
        from fcntl import ioctl
        from termios import TIOCGWINSZ
        from array import array

        winsize = array("H", [0] * 4)
        try:
            ioctl(sys.stdout.fileno(), TIOCGWINSZ, winsize)
        except IOError:
            pass
        return max(minimum, (winsize[1], winsize[0])[0])

    # the fall back value
    return max(minimum, default)


def marquee(msg=''):
    return ('{0:*^%s}' % console_width()).format(msg)


if __name__ == '__main__':

    w = console_width()
    print 'Console width:', w
    print '='*w

    def example():

        values = ['Paul Eden <paul@domain.com>',
                  'Eden Jones <ejones@domain.com>',
                  'Somebody Else <somebody@domain.com>']
        print 'substring completer example:'
        for x in values:
            print x

        substring_completer(values)

        while 1:
            a = raw_input('> ')
            print 'said:', a

    example()


