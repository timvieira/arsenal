The arsenal is an assortment of python utilities that I can't live without.

There are a lot of files here. I'd like to highlight a few of my most useful /
favorite things:

Highlights
----------

- `iterview.py`
    Progress bar for all iterables with a known length.

- `math/`
    Tons of math utilities

    ``math.compare`` is particularly useful for debugging numerical algorithms

- `terminal/`
    Utilities for making colorful and nicely formatting terminal output.

- `viz/`
    Utilities for making interactive plots, especially ``viz.util.{axman,lineplot}``.

- `alphabet.py`
    Maintain a bijective map from "things" to unique integers.

- `robust.py`
    Utilities such as ``timelimit`` and ``retry`` to help "robustify" your code.

- `fsutils.py`
    utilities for working with the file system like atomic file writes and
    recursively listing directories (like UNIX find)

- `debug/`
    I'm a big fan of ``debug.utils.ip``.

- `cache/`
    contains the ``memoize`` decorator and even a persistence shelve-based variant.
