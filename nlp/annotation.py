import re
from nlp.wordsplitter import wordsplit_sentence

class ParseError(Exception):
    """ Custom exception class used by this module. """
    pass

NEWLINE = '-NEWLINE-'

def _preprocess(x):
    "Warning: wordsplitter may alter non-whitespace characters in `x`."
    x = re.sub('\s+', ' ', x)    # collapse consecutive spaces
    x = wordsplit_sentence(x)    # apply wordsplitter
    return re.sub('(<[/]?[A-Za-z0-9]+>)', r' \1 ', x)

def xml2segments(x):
    """
    Generate a segmentation from an xml-style annotation.
    All the assumptions in `xml2bio` still apply.

    >>> x = xml2segments("<title>Cat in the Hat</title><author>Dr. Seuss</author>")
    >>> list(x)
    [('title', ['Cat', 'in', 'the', 'Hat']), ('author', ['Dr.', 'Seuss'])]
    """
    x = _preprocess(x)
    for label, tagged, close, word in re.findall('(?:(?:\s*<([A-Za-z0-9]+)>\s*([\w\W]+?)\s*</([A-Za-z0-9]+)>\s*)|([\w\W]+?)(?:\s+|$))', x):
        if close != label:
            raise ParseError('Mismatched xml tags (%s, %s)' % (close, label))
        if word:
            yield ('O', [word])
        else:
            yield (label, tagged.split())

def xml2bio(x):
    """
    Generate BIO-token pairs from xml-style annotation.
    Notes:
      1) Splits text on spaces, so wordsplitting should already be done.
      2) Assumes no self-closing tags
      3) Assumes no nesting (tags within tags)
      4) Converts newlines into a token "-NEWLINE-"

    >>> x = xml2bio("<title>Cat in the Hat</title><author>Dr. Seuss</author>")
    >>> list(x)                                  #doctest:+NORMALIZE_WHITESPACE
    [('B-title', 'Cat'), ('I-title', 'in'), ('I-title', 'the'), 
     ('I-title', 'Hat'), ('B-author', 'Dr.'), ('I-author', 'Seuss')]
    """
    x = _preprocess(x)
    for label, tagged, close, word in re.findall('(?:(?:\s*<([A-Za-z0-9]+)>\s*([\w\W]+?)\s*</([A-Za-z0-9]+)>\s*)|([\w\W]+?)(?:\s+|$))', x):
        if close != label:
            raise ParseError('Mismatched xml tags (%s, %s)' % (close, label))
        if word:
            yield ('O', word)
        else:
            words = iter(tagged.split())
            yield ('B-%s' % label, words.next())
            for w in words:
                yield ('I-%s' % label, w)

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
            yield ('B-%s' % label, words.next())
            for w in words:
                if '[' in w or ']' in w:
                    raise ParseError('brackets can not appear within a word.')
                yield ('I-%s' % label, w)

# TIMV: we want something like a LineGroupIterator
# TDOD: make this
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


from collections import namedtuple
Span = namedtuple('Span', 'label begins ends')

# TIM: add an option for strict BIO sequences, no heuristics
def bio2span(seq, tagger=None, include_O=True):
    """
    Given a sequence and a function for grabbing labels, return a list of `Spans`.
    Note: Will interpret `None` as "O"

    >>> bio2span(['O','B-NUM','B-DATE', 'I-DATE'], include_O=False)
    [Span(label='NUM', begins=1, ends=2), Span(label='DATE', begins=2, ends=4)]

    `bio2span` will apply some heuristics for bad BIO sequences.
    For example:
      >>> bio2span(['O','B-NUM','I-DATE'], include_O=False)
      [Span(label='NUM', begins=1, ends=2), Span(label='DATE', begins=2, ends=3)]
    """
    if tagger is not None:
        seq = [tagger(tk) for tk in seq]
    phrase = []
    phrases = []
    intag = None
    for i, lbl in enumerate(seq):
        if lbl is None:
            lbl = 'O'
        if lbl.startswith('B-'):
            if intag and len(phrase):
                phrases.append(phrase)
                phrase = []
            intag = lbl[2:]
            phrase = [intag, i]
        elif lbl.startswith('I-'):
            if intag == lbl[2:]:             # and youre still in the same span
                phrase.append(i)
            else:                            # you're in a new span (hueristic correction)
                if len(phrase):
                    phrases.append(phrase)
                intag = lbl[2:]
                phrase = [intag, i]
        elif intag:                          # was in tag, now outiside ("O")
            intag = None
            phrases.append(phrase)
            phrases.append(i)
            phrase = []
        else:
            phrases.append(i)
    if intag and len(phrase):                # close any lingering spans
        phrases.append(phrase)
    if include_O:
        ret = []
        for s in phrases:
            if isinstance(s, list):
                ret.append(Span(s[0], s[1], s[-1]+1))
            else:
                ret.append(Span('O', s, s+1))
    else:
        ret = [Span(s[0], s[1], s[-1]+1) for s in phrases if isinstance(s, list)]
    return ret


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    from nlp.tests.bio2spantest import test_bio2span
    test_bio2span()
