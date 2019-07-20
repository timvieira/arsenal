import re
from sys import stdout, stderr, stdin
from glob import glob
from io import StringIO

def print_parse(t, out=stdout.write):
    "Print parse formatted as an s-expression."
    def pp(t):
        if isinstance(t, str):                    # base case
            return out(t)
        if len(t) == 1:
            if t[0]:
                pp(t[0])
            return
        label, children = t[0], t[1:]
        assert isinstance(label, str)
        out('(%s ' % label)
        n = len(children)
        for i, child in enumerate(children):
            pp(child)   # first child already indented
            if i != n-1:                                 # no space after last child
                out(' ')
        out(')')
    pp(t)
    out('\n')


def pprint(t, out=stdout.write):
    "Pretty print tree as a tabbified s-expression."
    def pp(t, indent=0, indentme=True):
        if indentme:
            out(' '*indent)
        if isinstance(t, str):                    # base case
            return out(t)
        if len(t) == 1:
            if t[0]:
                pp(t[0], indent, indentme)
            return
        label, children = t[0], t[1:]
        assert isinstance(label, str)
        out('(%s ' % label)
        n = len(children)
        for i, child in enumerate(children):
            pp(child, indent + len(label) + 2, i != 0)   # first child already indented
            if i != n-1:                                 # no newline after last child
                out('\n')
        out(')')
    pp(t)
    out('\n')


def pformat(t):
    "Pretty print tree as a tabbified s-expression."
    y = StringIO()
    pprint(t, out=y)
    return y.getvalue()


def sexpr(s, add_root=True):
    """

    Example usage:

      >>> sexpr('(S (NP Papa) (VP (V ate) (NP (Det the) (N caviar))))')
      ['S', ['NP', 'Papa'], ['VP', ['V', 'ate'], ['NP', ['Det', 'the'], ['N', 'caviar']]]]


    TO match the Penn tree bank we add a ROOT symbol in the following case

      >>> sexpr('((S (NP Papa) (VP (V ate) (NP (Det the) (N caviar)))))')
      ['ROOT', ['S', ['NP', 'Papa'], ['VP', ['V', 'ate'], ['NP', ['Det', 'the'], ['N', 'caviar']]]]]

    """


    s = s[s.find('('):]
    tree = []
    stack = []  # top of stack (index -1) points to current node in tree
    stack.append(tree)
    curtok = ""
    depth = 0
    for c in s:
        if c=='(':
            new = []
            stack[-1].append(new)
            stack.append(new)
            curtok = ""
            depth += 1
        elif c==')':
            if curtok:
                stack[-1].append(curtok)
                curtok = ""
            stack.pop()
            curtok = ""
            depth -= 1
        #elif c.isspace():
        elif c in (' ','\t','\r','\n'):  ## dont want funny unicode ones?
            if curtok:
                stack[-1].append(curtok)
                curtok = ""
        else:
            curtok += c
        if depth < 0:
            raise BadSexpr("Too many closing parens")
    if depth > 0:
        raise BadSexpr("Didn't close all parens, depth %d" % depth)
    root = tree[0]
    # weird, treebank parses have an extra, unlabeled node on top
    if isinstance(root[0], list) and add_root:
        root = ["ROOT"] + root
    return root

class BadSexpr(Exception):
    pass



#def features(t):
#    print 'S, NP, VP'


def main():

    for filename in glob('/home/timv/projects/ldp/data/LDC99T42/treebank_3/parsed/mrg/wsj/*/*.mrg'):
        #print >> stderr, filename
        print('.', end=' ', file=stderr)

        with open(filename) as f:
            contents = f.read()
            chunks = contents.split('( (')

        # parse file using sexpr
        for chunk in chunks:

            if not chunk.strip():
                continue

            chunk = '( (' + chunk

            print(chunk)

            try:
                tree = sexpr(chunk)
            except BadSexpr:
                print(file=stderr)
                print('failed to parse tree', file=stderr)
                print(chunk, file=stderr)
                continue

            print(tree)

        return



if __name__ == '__main__':
    main()
