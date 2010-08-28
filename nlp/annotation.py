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

def grouper(text, pattern):
    """
    Very simple function for breaking up text into groups based on a 
    single pattern.

    >>> list(grouper("a BB c d BB", "BB"))
    ['a', 'c d']
    """
    for group in re.split(pattern, text):    # TODO: make this "lazier"
        group = group.strip()
        if group:
            yield group

if __name__ == '__main__':
    import doctest
    doctest.testmod()

