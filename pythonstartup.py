"""

This module provides some tiny subset of the nice stuff that the IPython shell
provides, but is much lighter weight and does not require installing stuff.

To use this set a environment variable PYTHONSTARTUP=<path-to-this-file>

"""

import os
import re
import sys


## TODO: add support for autoreload


def setup():
    """ Set-up some interactive features """

    __builtins__._H = [None]
    class Prompt:
        def __init__(self):
            self.str = '[%d]$ '    #'\001\033[0:1;31m\002h[%d] >>> \001\033[0m\002'
        def __str__(self):
            if hasattr(__builtins__, '_'):  # initially '_' this is not there.
                __builtins__._H.append(__builtins__._)
            return self.str % len(__builtins__._H)
        def __radd__(self, other):
            return str(other) + str(self)

    class Prompt2:
        def __str__(self):
            return '.'*len(str(sys.ps1))
        def __radd__(self, other):
            return str(other) + str(self)

    sys.ps1 = Prompt()
    sys.ps2 = Prompt2()

    #sys.excepthook = LazyPython()
    
    # Pretty-print at the command prompt for more readable dicts and lists.
    from pprint import pprint
    def my_displayhook(val):
        if val is not None:
            __builtins__._ = val
            pprint(val)
    sys.displayhook = my_displayhook


    # Try to set up command history completion, saving, and reloading
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        import rlcompleter
        readline.parse_and_bind("tab: complete")

        # The place to store your command history between sessions
        histfile = os.environ['HOME'] + '/.python-history'

        readline.read_history_file(histfile)

        # atexit module does not seem to cover all cases of exiting (at least in cygwin)
        import atexit       # "at exit"
        @atexit.register
        def savehist():
            try:
                readline.write_history_file(histfile)
            except:
                print 'Unable to save Python command history'

# SET IT UP!
setup()
from pydoc import help


