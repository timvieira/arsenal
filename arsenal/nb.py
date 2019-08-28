"""
Utilities for working with Jupyter notebooks.
"""

from inspect import getsource
from IPython.display import HTML, display


def psource(*functions):
    """
    Print the source code for the given function(s).

    Based on https://github.com/aimacode/aima-python/blob/master/notebook.py

    """
    source_code = '\n\n'.join(getsource(fn) for fn in functions)
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer
        from pygments import highlight

        display(HTML(highlight(source_code, PythonLexer(), HtmlFormatter(full=True))))

    except ImportError:
        print(source_code)
