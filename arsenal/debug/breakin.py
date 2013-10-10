# Copyright (C) 2006, 2007, 2009 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

# [TIMV] changes:
#   * removed deprecated function hook_sigquit
#   * aliased `hook_debugger_to_signal -> `enable` now its easier to remember


import sys, signal
from contextlib import contextmanager
from arsenal.debug.utils import ip, set_trace

_breakin_signal_number = None
_breakin_signal_name = None

def determine_signal():
    global _breakin_signal_number
    global _breakin_signal_name
    if _breakin_signal_number is not None:
        return _breakin_signal_number
    # Note: As near as I can tell, Windows is the only one to define SIGBREAK,
    #       and other platforms defined SIGQUIT. There doesn't seem to be a
    #       platform that defines both.
    #       -- jam 2009-07-30
    sigquit = getattr(signal, 'SIGQUIT', None)
    sigbreak = getattr(signal, 'SIGBREAK', None)
    if sigquit is not None:
        _breakin_signal_number = sigquit
        _breakin_signal_name = 'SIGQUIT'
    elif sigbreak is not None:
        _breakin_signal_number = sigbreak
        _breakin_signal_name = 'SIGBREAK'
    return _breakin_signal_number


def hook_to_signal(handler):
    """Add a signal handler so we drop into the debugger.

    On Linux and Mac, this is hooked into SIGQUIT (C-\\) on Windows, this is
    hooked into SIGBREAK (C-Pause).
    """
    # when sigquit (C-\) or sigbreak (C-Pause) is received go into pdb
    sig = determine_signal()
    if sig is None:
        from warnings import warn
        warn('System does not support the signals required to enable breakin.')
        return
    signal.signal(sig, handler)


@contextmanager
def breakin_ctx(frame):
    import traceback
    sys.stderr.write('** Breaking in to running process **\n'
                     'Traceback:\n%s'
                     % (''.join(traceback.format_stack(frame))))

    d = {'_frame': frame}        # Allow access to frame object.
    d.update(frame.f_globals)    # Unless shadowed by global
    d.update(frame.f_locals)

    # It seems that on Windows, when sys.stderr is to a PIPE, then we need to
    # flush. Not sure why it is buffered, but that seems to be the case.
    sys.stderr.flush()
    # restore default meaning so that you can kill the process by hitting it twice
    signal.signal(_breakin_signal_number, signal.SIG_DFL)
    try:
        yield d
    finally:
        signal.signal(_breakin_signal_number, shell)


# [TIMV] ideas:
#   * I'm not crazy about being dropped into `_debug`'s frame - it would
#     probably be more useful to land in the interrupted frame
def debug(signal_number, frame):
    with breakin_ctx(frame):
        sys.stderr.write("** Type 'c' to continue or 'q' to stop the process\n")
        set_trace()


def shell(sig, frame):
    """Interrupt running process and provide a python prompt for debugging."""
    with breakin_ctx(frame) as d:
        ip(local_ns=d)


# TIMV: alias (much easier to remember)
#enable = lambda: hook_to_signal(debug)
enable = enable_shell = lambda: hook_to_signal(shell)


if __name__ == '__main__':

    import time
    def example():
        myvar = 'Break-in should be able to see me in the shell!'
        N = 8
        print 'You have %s seconds to hit \C-\\' % N
        for i in reversed(xrange(N)):
            print i, '..',
            time.sleep(1)
            sys.stdout.flush()

    enable()

    example()
