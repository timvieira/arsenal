from collections import defaultdict

class LexiconToken(object):

    def __init__(self, w):
        self.form = w
        self.next = None
        self.prev = None

    def __repr__(self):
        return 'LexiconToken(%s)' % self.form


class Lexicon(object):

    def __init__(self, filename, key=lambda x: x.lower()):
        self.contents = defaultdict(list)
        self.key = key
        with file(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    # create LexiconTokens and set their next and prev pointers
                    tokens = []
                    t = None
                    for w in line.split():
                        t2 = LexiconToken(self.key(w))
                        t2.prev = t
                        if t is not None:
                            t.next = t2
                        t = t2
                        tokens.append(t2)
                    # add tokens to lexicon
                    for tk in tokens:
                        self.__iadd__(tk)

    def __iadd__(self, t):
        if isinstance(t, basestring):
            t = LexiconToken(self.key(t))
        self.contents[self.key(t.form)].append(t)

    def contains(self, query):
        """Is query in the lexicon, accounting for lexicon phrases and the context."""

        def xx(x):
            fullentry = []
            while x:
                fullentry.append(x)
                x = x.next
            return fullentry

        for entry in self.contents[self.key(query.form)]:

            te = entry
            tq = query
            result = True

            # Go the beginning of this lexicon entry
            while te.prev and result:
                if not tq.prev:
                    return False
                te = te.prev
                tq = tq.prev

            # Check for match all the way to the end of this lexicon entry
            doWhileHack = True
            while te and tq and result or doWhileHack:
                if te.form != self.key(tq.form):
                    result = False
                te = te.next
                tq = tq.next
                doWhileHack = False
            if result and not te:
                return True

        return False


def test():
    lex = Lexicon('lexicon/US-states')

    from textmill.representation import Instance

    seq = Instance.from_sgml("Welcome to South DaKota")
    assert lex.contains(seq.sequence[2])
    assert lex.contains(seq.sequence[3])

    seq = Instance.from_sgml("South")
    assert not lex.contains(seq.sequence[0])

    seq = Instance.from_sgml("North")
    assert not lex.contains(seq.sequence[0])


if __name__ == '__main__':
    test()
