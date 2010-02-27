"""
Draw inheritance hierarchies via Dot (http://www.graphviz.org/)
Author: Michele Simionato
E-mail: mis6@pitt.edu
Date: August 2003
License: Python-like
Requires: Python 2.3, dot, standard Unix tools
"""

import os
import itertools

PSVIEWER = 'evince'
PNGVIEWER = 'kview'
PSFONT = 'Times'
PNGFONT = 'Courier'


def MRO(cls):
    "Returns the MRO of cls as a text"
    out = ["MRO of %s:" % cls.__name__]
    for counter, c in enumerate(cls.__mro__):
        name = c.__name__
        bases = ','.join([b.__name__ for b in c.__bases__])
        s = "  %s - %s(%s)" % (counter, name, bases)
        if type(c) is not type:
            s += "[%s]" % type(c).__name__
        out.append(s)
    return '\n'.join(out)


class MROgraph(object):

    def __init__(self, *classes, **options):
        """Generates the MRO graph of a set of given classes."""
        if not classes:
            raise Exception('Missing class argument!')
        filename = options.get('filename', "MRO_%s.ps" % classes[0].__name__)
        self.labels = options.get('labels', 2)
        caption = options.get('caption', '')
        setup = options.get('setup', '')
        name, dotformat = os.path.splitext(filename)
        format = dotformat[1:]
        fontopt = "fontname=" + (PSFONT if format == 'ps' else PNGFONT)
        nodeopt = ' node [%s];\n' % fontopt
        edgeopt = ' edge [%s];\n' % fontopt
        viewer = PSVIEWER if format == 'ps' else PNGVIEWER
        self.textrepr = '\n'.join([MRO(cls) for cls in classes])
        if caption:
            caption = ('caption [shape=box,label="%s\n",fontsize=9];'
                       % self.textrepr).replace('\n', '\\l')
        setupcode = nodeopt + edgeopt + caption + '\n' + setup + '\n'
        codeiter = itertools.chain(*[self.genMROcode(cls) for cls in classes])
        self.dotcode = \
            'digraph %s{\n%s%s}' % (name, setupcode, '\n'.join(codeiter))
        os.system("echo '%s' | dot -T%s > %s; %s %s&" % (self.dotcode,
                                                         format,
                                                         filename,
                                                         viewer,
                                                         filename))

    def genMROcode(self, cls):
        "Generates the dot code for the MRO of a given class"
        for mroindex, c in enumerate(cls.__mro__):
            name = c.__name__
            manyparents = len(c.__bases__) > 1

            if c.__bases__:
                yield ''.join(' edge [style=solid]; %s -> %s %s;\n' % (
                    b.__name__, name,
                    ('[label="%s"]' % (i+1)) \
                        if manyparents and self.labels == 2 \
                        else '')
                    for i, b in enumerate(c.__bases__))

            if manyparents:
                yield " {rank=same; %s}\n" \
                    % ''.join('"%s"; ' % b.__name__ for b in c.__bases__)

            number = "%s-" % mroindex if self.labels else ''
            label = 'label="%s"' % (number + name)

            # if cls is a metaclass use a box
            option = '[%s]' if issubclass(cls, type) else '[shape=box,%s]'

            yield(' %s %s;\n' % (name, option % label))

            if type(c) is not type: # c has a custom metaclass
                metaname = type(c).__name__
                yield ' edge [style=dashed]; %s -> %s;' % (metaname, name)

    def __repr__(self):
        "Returns the Dot representation of the graph"
        return self.dotcode

    def __str__(self):
        "Returns a text representation of the MRO"
        return self.textrepr


def testHierarchy(**options):
    class M(type): pass # metaclass
    class F(object): pass
    class E(object): pass
    class D(object): pass
    class G(object): __metaclass__ = M
    class C(F,D,G): pass
    class B(E,D): pass
    class A(B,C): pass
    return MROgraph(A,M,**options)

if __name__ == "__main__":
    testHierarchy() # generates a postscript diagram of A and M hierarchies
