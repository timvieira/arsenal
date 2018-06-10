import re
from arsenal.misc import force


class ParseError(Exception):
    """ Custom exception class used by this module. """
    pass

class Span(object):
    __slots__ = ('label','begins','ends')
    def __init__(self, label, begins, ends):
        self.label = label
        self.begins = begins
        self.ends = ends
    def __repr__(self):
        return 'Span(label=%r, begins=%r, ends=%r)' % (self.label, self.begins, self.ends)
    def __eq__(self, other):
        if isinstance(other, Span):
            return (self.label == other.label and self.begins == other.begins and self.ends == other.ends)
        else:
            return len(other) == 3 and (self.label == other[0] and self.begins == other[1] and self.ends == other[2])
    def __iter__(self):
        return iter((self.label, self.begins, self.ends))


WhitespaceLexer = re.compile('\S+')

Lexer = re.compile('|'.join(["http://\S+",                               # keep urls together.. might include invalid URL characters
                             "\S+@\S+",
                             "[0-9][0-9]?\s*\([0-9]?\)",                 # e.g. "7(4)" common in volume
                             "\(\s*[0-9][0-9]?\s*\)",                    # e.g. "(4)" common in volume
                             "[0-9]+\s*-\s*[0-9]+",                      # possible page number
                             "[0-9]+(?:st|nd|rd|th)",
                             "[A-Z]\.",
                             "Ph\.?[Dd]\.",
                             #"[Vv]ol(?:\.|ume)\s*[0-9]+",               # make "Vol. 3" one token.
                             "(?:Vol|Proc|Dept|Univ|No|Inc|Dr)\s*\.",
                             "pp\.",
                             "\(\s*[0-9][0-9][0-9][0-9][a-z]?\s*\)",     # e.g. "(1994)" year in parens
                             "[Ee]d(?:s?\.|itors?)",
                             #"\w+-\w+",
                             "\+[A-Z]+\+",
                             "[a-zA-Z]+(?:'s)?",
                             #"[0-9]+(?:\.[0-9]+)?",                      # 231 or 2.0, but not 2.
                             "[0-9]+",
                             "[()\"'\-\.,]",
                             "\S+"]))

TaggedText = re.compile("<([a-z0-9_]+)>([\w\W]+?)</([a-z0-9_]+)>|([^<>\s]+)", re.IGNORECASE)

def fromSGML(f, linegrouper="\n", bioencoding=False):
    for line in re.split(linegrouper, open(f).read()):
        if bioencoding:
            seq = sgml2bio(line)
        else:
            seq = sgml2seq(line)
        if seq:
            yield seq

@force
def sgml2segmentation(x, lexer=WhitespaceLexer):
    """
    >>> sgml2segmentation('<title>Cat in the Hat</title><author>Dr. Seuss</author>')
    [('title', ['Cat', 'in', 'the', 'Hat']), ('author', ['Dr.', 'Seuss'])]
    """
    x = x.strip().replace("\n", " +L+ ")
    for (tag, tagged, close, outside) in TaggedText.findall(x):
        if tag != close:
            raise ParseError("opening (%s) and closing (%s) tags do not match in sequence\n    %r\n" % (tag, close, x))
        if tagged:
            yield (tag, lexer.findall(tagged))
        else:
            for w in lexer.findall(outside):
                yield ("O", [w])

@force
def sgml2bio(x):
    """
    >>> sgml2bio('<title>Cat in the Hat</title><author>Dr. Seuss</author>')
    [('B-title', 'Cat'), ('I-title', 'in'), ('I-title', 'the'), ('I-title', 'Hat'), ('B-author', 'Dr.'), ('I-author', 'Seuss')]
    """
    for (tag, tokens) in sgml2segmentation(x):
        tokens = iter(tokens)
        yield ('B-' + tag, next(tokens))
        for w in tokens:
            yield ('I-' + tag, w)

@force
def sgml2seq(x):
    """
    >>> sgml2seq('<title>Cat in the Hat</title><author>Dr. Seuss</author>')
    [('title', 'Cat'), ('title', 'in'), ('title', 'the'), ('title', 'Hat'), ('author', 'Dr.'), ('author', 'Seuss')]
    """
    for (tag, tokens) in sgml2segmentation(x):
        for w in tokens:
            yield (tag, w)

def bracket2bio(x):
    """
    generate BIO-token pairs from bracket-style annotation.
    Note: splits text of spaces, so wordsplitting should already be done.

    >>> x = bracket2bio("[TITLE Cat in the Hat][AUTHOR Dr. Seuss]")
    >>> list(x)                                  #doctest:+NORMALIZE_WHITESPACE
    [('B-TITLE', 'Cat'), ('I-TITLE', 'in'), ('I-TITLE', 'the'),
     ('I-TITLE', 'Hat'), ('B-AUTHOR', 'Dr.'), ('I-AUTHOR', 'Seuss')]
    """
    if '\n' in x:
        raise ParseError('No newlines allowed in brack2bio annotation.')
    for label, tagged, word in re.findall('(?:(?:\[([A-Z0-9]+)\s+(.+?)\s*\]\s*)|(.+?)(?:\s+|$))', x):
        if word:
            yield ('O', word)
        else:
            words = iter(tagged.split())
            yield ('B-%s' % label, next(words))
            for w in words:
                if '[' in w or ']' in w:
                    raise ParseError('brackets can not appear within a word.')
                yield ('I-%s' % label, w)

# TIMV: we want something like a LineGroupIterator
def line_groups(text, pattern):
    """
    Very simple function for breaking up text into groups based on a
    single pattern.

    >>> list(line_groups("a BB c d BB", "BB"))
    ['a', 'c d']
    """
    for group in re.split(pattern, text):    # TODO: make this "lazier"
        group = group.strip()
        if group:
            yield group


def extract_contiguous(s, labeler=None):
    """
    >>> list(extract_contiguous(""))
    []

    >>> list(extract_contiguous("AAAA"))
    [Span(label='A', begins=0, ends=4)]

    >>> list(extract_contiguous("AABBC"))
    [Span(label='A', begins=0, ends=2), Span(label='B', begins=2, ends=4), Span(label='C', begins=4, ends=5)]

    >>> list(extract_contiguous("AABBB"))
    [Span(label='A', begins=0, ends=2), Span(label='B', begins=2, ends=5)]
    """
    if labeler is not None:
        s = map(labeler, s)
    prev = None
    b = e = 0
    for e, token in enumerate(s):
        if token != prev:
            if prev is not None:
                yield Span(prev, b, e)
            b = e
        prev = token
    # emit lingering bits
    if prev is not None:
        yield Span(prev, b, e + 1)


@force
def bio2span(seq, tagger=None, include_O=True):
    if tagger is not None:
        seq = map(tagger, seq)
    phrase = None
    intag = None
    for i, lbl in enumerate(seq):
        if lbl is None:
            lbl = 'O'
        label = lbl[2:]
        if lbl.startswith('B-'):
            if intag and phrase:
                yield phrase
            phrase = Span(label, i, i + 1)
        elif lbl.startswith('I-'):
            if intag == label:             # and youre still in the same span
                phrase.ends = i + 1
            else:                          # you're in a new span (hueristic correction)
                if phrase:
                    yield phrase
                phrase = Span(label, i, i + 1)
        else:
            if intag:                      # was in tag, now outiside ("O")
                if phrase:
                    yield phrase
                phrase = None
            if include_O:
                yield Span(lbl, i, i + 1)
        if lbl == 'O':
            intag = None
        else:
            intag = label
    if intag and phrase:                   # close any lingering spans
        yield phrase


if __name__ == '__main__':
    from arsenal.misc import piped
    def main():
        for line in piped() or []:
            for (label, w) in sgml2bio(line):
                print('%s\t%s' % (label, w))
            print()
    main()
