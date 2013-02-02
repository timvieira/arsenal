#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from text import markup


_whitespace_cleanup = re.compile('[ ]*\n', re.MULTILINE)
def whitespace_cleanup(x):
    return _whitespace_cleanup.sub('\n', x)


# Borrowed from: http://www.codigomanso.com/en/2010/05/una-de-python-force_unicode/
def force_unicode(s, encoding='utf-8', errors='ignore'):
    """
    Returns a unicode object representing 's'. Treats bytestrings using the
    'encoding' codec.
    """
    if s is None:
        return u''
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join(force_unicode(arg, encoding, errors) for arg in s)
        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError (s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join(force_unicode(arg, encoding, errors) for arg in s)
    return unicode(s)


def PRE(x):
    return '<pre>' +  x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + '</pre>'


# native, HTML, default Unicode (Code page 850), Unicode combined Character, Windows-1250
"""
_recodings = {'ae': ['ä', u'ä', '&auml;', '\u00E4', u'\u00E4', '\u0308a', '\xc3\xa4'],
              'oe': ['ö', u'ö', '&ouml;', '\u00F6', u'\u00F6', '\u0308o', '\xc3\xb6'],
              'ue': ['ü', u'ü', '&uuml;', '\u00FC', u'\u00FC', '\u0308u', '\xc3\xbc'],
              'Ae': ['Ä', u'Ä', '&Auml;', '\u00C4', u'\u00C4', '\u0308A', '\xc3\x84'],
              'Oe': ['Ö', u'Ö', '&Ouml;', '\u00D6', u'\u00D6', '\u0308O', '\xc3\x96'],
              'Ue': ['Ü', u'Ü', '&Uuml;', '\u00DC', u'\u00DC', '\u0308U', '\xc3\x9c'],
              'ss': ['ß', u'ß', '&szlig;', '\u00DF', u'\u00DF', '\xc3\x9f'],
              'e': ['é', u'é', '\xc3\xa9'],
             }
"""

# taken from NLTK
def htmltotext(x):
    """ Remove HTML markup from the given string. """
    # remove inline JavaScript / CSS
    x = re.compile('<script.*?>[\w\W]*?</script>', re.IGNORECASE).sub('', x)
    x = re.compile('<style.*?>[\w\W]*?</style>', re.IGNORECASE).sub('', x)
    # remove html comments. must be done before removing regular tags since comments can contain '>' characters.
    x = re.sub(r'<!--([\w\W]*?)-->', '', x)
    # remove the remaining tags
    x = re.sub(r'(?s)<.*?>', ' ', x)
    # remove html entities
    x = markup.remove_entities(x)
    # clean up whitespace
    x = re.sub('[ ]+', ' ', x)
    x = re.compile('(\n\n+)', re.MULTILINE).sub('\n', x)
    return x


import unicodedata
def strip_accents(s):
    """ Transform accentuated unicode symbols into their simple counterpart. """
    return u''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

# iso-8859-1
LATIN2ASCII = {
    # uppercase
    u'\u00c0': 'A`',
    u'\u00c1': "A'",
    u'\u00c2': 'A^',
    u'\u00c3': 'A~',
    u'\u00c4': 'A:',
    u'\u00c5': 'A%',
    u'\u00c6': 'AE',
    u'\u00c7': 'C,',
    u'\u00c8': 'E`',
    u'\u00c9': "E'",
    u'\u00ca': 'E^',
    u'\u00cb': 'E:',
    u'\u00cc': 'I`',
    u'\u00cd': "I'",
    u'\u00ce': 'I^',
    u'\u00cf': 'I:',
    u'\u00d0': "D'",
    u'\u00d1': 'N~',
    u'\u00d2': 'O`',
    u'\u00d3': "O'",
    u'\u00d4': 'O^',
    u'\u00d5': 'O~',
    u'\u00d6': 'O:',
    u'\u00d8': 'O/',
    u'\u00d9': 'U`',
    u'\u00da': "U'",
    u'\u00db': 'U~',
    u'\u00dc': 'U:',
    u'\u00dd': "Y'",
    u'\u00df': 'ss',
    # lowercase
    u'\u00e0': 'a`',
    u'\u00e1': "a'",
    u'\u00e2': 'a^',
    u'\u00e3': 'a~',
    u'\u00e4': 'a:',
    u'\u00e5': 'a%',
    u'\u00e6': 'ae',
    u'\u00e7': 'c,',
    u'\u00e8': 'e`',
    u'\u00e9': "e'",
    u'\u00ea': 'e^',
    u'\u00eb': 'e:',
    u'\u00ec': 'i`',
    u'\u00ed': "i'",
    u'\u00ee': 'i^',
    u'\u00ef': 'i:',
    u'\u00f0': "d'",
    u'\u00f1': 'n~',
    u'\u00f2': 'o`',
    u'\u00f3': "o'",
    u'\u00f4': 'o^',
    u'\u00f5': 'o~',
    u'\u00f6': 'o:',
    u'\u00f8': 'o/',
    u'\u00f9': 'o`',
    u'\u00fa': "u'",
    u'\u00fb': 'u~',
    u'\u00fc': 'u:',
    u'\u00fd': "y'",
    u'\u00ff': 'y:',
}


LIGATURES_PAIRS = [
    (u'ﬃ', 'ffi'),
    (u'ﬀ', 'ff'),
    (u'ﬁ', 'fi'),
    (u'ﬂ', 'fl'),

    (u'—', '--'),
    (u'–', '-'),

    (u'“', '"'),
    (u'”', '"'),

    (u" ", " "),
    (u"’", "'"),
    (u"•", "*"),
    (u"…", "..."),

    (u'\u00c6', 'AE'),
    (u'\u00e6', 'ae'),
    (u'\u0152', 'OE'),
    (u'\u0153', 'oe'),
    (u'\u0132', 'IJ'),
    (u'\u0133', 'ij'),
    (u'\u1d6b', 'ue'),
    (u'\ufb00', 'ff'),
    (u'\ufb01', 'fi'),
    (u'\ufb02', 'fl'),
    (u'\ufb03', 'ffi'),
    (u'\ufb04', 'ffl'),
    (u'\ufb05', 'ft'),
    (u'\ufb06', 'st'),
]

LIGATURES_MAP = dict(LIGATURES_PAIRS)

LIGATURES = re.compile(u'(%s)' % u'|'.join(k for k,v in LIGATURES_PAIRS))


#import unicodedata
#>>> source = u'Mikael Håfström'
#>>> unicodedata.normalize('NFKD', source).encode('ascii', 'ignore')
def normalize(text):
    u"""
    >>> normalize(u'Efﬁciently')
    u'Efficiently'
    """
    text = force_unicode(text)
    return unicodedata.normalize('NFKD', text) #.encode('ascii', 'ignore')


def remove_ligatures(text):
    u"""
    >>> remove_ligatures(u'Efﬁciently')
    u'Efficiently'
    """
    text = normalize(text)   # or at least force_unicode
    return LIGATURES.sub(lambda m: LIGATURES_MAP[m.group(1)], text)


def convert_special_html_escapes(text):
    for plain, funny in (('ä','&auml;'), ('ö','&ouml;'), ('ü','&uuml;'), ('Ä','&Auml;'), ('Ö','&Ouml;'),
                         ('Ü','&Uuml;'), ('ß','&szlig;')):
        text = text.replace(funny, plain)
    return text


def remove_html_escapes(text):
    for plain, funny in (('&','&amp;'), ('<','&lt;'), ('>','&gt;'), ('"','&quot;'), ("'",'&#39;')):
        text = text.replace(funny, plain)
    return text


def remove_latin(text):
    text = text.encode('utf-8')
    text = unicode(text)
    # chars that ISO-8859-1 does not support
    for plain, funny_set in (
                             ('"', u'“”'),
                             ('-', u'\u2013\u2014\u2022'),
                             ("'", u'\u2018\u2019'),
                             ('', u'\ufffd\u2122\u2020'),
                             ('...', u'\u2026'),
#                             ('i', u'\u012b'),
#                             ('ã', u'\u0101'),
#                             ('r', u'\u0159'),
#                             ('Z',u'\u017d'),
#                             ('z', u'\u017e'),
                             ('EUR', u'\u20ac')):
        for funny in funny_set:
            orig = text
            text = text.replace(funny, plain)
            if orig != text:
                print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                print funny, '->', plain
                print list(funny_set)
                print text
                print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    return text

def remove_accents(text):
    text = unicode(text).encode('utf-8')
    for plain, funny_set in (('a','áàâãäå\u0101'), ('e','éèêẽë'), ('i',"íìîĩï"), ('o','óòôõöø'),
                             ('u',"úùûũü"), ('A','ÁÀÂÃÄÅ'), ('E','ÉÈÊẼË'), ('I',"ÍÌÎĨÏ"),
                             ('O','ÓÒÔÕÖØ'), ('U',"ÚÙÛŨÜ"), ('n',"ñ"), ('c',"ç"), ('N',"Ñ"),
                             ('C',"Ç"), ('d',"Þ"), ('ss',"ß"), ('ae',"æ"), ('oe','œ')):
        for funny in funny_set:
            text = text.replace(funny, plain)
    return text



if __name__ == '__main__':
    import sys

    if sys.stdin.isatty():
        sys.exit(1)

    x = sys.stdin.read()
    #x = htmltotext(x)

    x = remove_ligatures(x).encode('ascii', 'ignore')

    print x
