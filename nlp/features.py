import re

from arsenal.nlp import gazetteers

class pattern(object):
    """
    Utility for common regex things...

    Note: regular expressions are always compiled with the VERBOSE flag.
    """
    def __init__(self, p, handler=lambda *x: bool(x or True), flags=re.IGNORECASE):
        self.re_matches  = re.compile('^%s$' % p, re.VERBOSE|flags)
        self.re_contains = re.compile('.*?%s.*?' % p, re.VERBOSE|flags)
        self._handler = handler

    def handler(self, *args):
        # need to strip off self argument
        return self._handler(*args)

    def contains(self, x):
        if hasattr(x, 'form'): x = x.form
        m = self.re_contains.match(x)
        if m: return self.handler(*m.groups())

    def matches(self, x):
        if hasattr(x, 'form'): x = x.form
        m = self.re_matches.match(x)
        if m: return self.handler(*m.groups())

    __call__ = matches


## maybe i want to distinguish between sometimes and always ordinals
ordinal = pattern("""
    (?:
        \d+(?:st|nd|rd|th)
        |first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth
        |eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth
        |seventeenth|eighteenth|nineteenth
        |twentieth|thirtieth|fou?rtieth|fiftieth|sixtieth|seventieth
        |eightieth|ninetieth
        |hundredth|thousandth|millionth|billionth
    )
    """)

fraction_denom = pattern("""
    (?:
        half|halve|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth
        |eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth
        |seventeenth|eighteenth|nineteenth
        |twentieth|thirtieth|fou?rtieth|fiftieth|sixtieth|seventieth
        |eightieth|ninetieth
        |hundredth|thousandth|millionth|billionth
    )s   # <-- NOTE the 's'
    """)

written_number = pattern('|'.join(gazetteers.numbers))

digits = pattern('(\d+)')
four_digits = pattern('(\d\d\d\d)')
two_digits = pattern('(\d\d)')

two_letter = pattern('[A-Z][A-Z]')
initial = pattern('[A-Z]\.')
abbrev = pattern('([A-Z]?[a-z]+\.)')
punct = pattern('[!"#&\'\(\)/:;<>\?@\[\]\_`{\|}~^]+')
alpha = pattern('[A-Za-z]+')
roman = pattern("""
    (M?M?M?(?:CM|CD|D?C?C?C?)(?:XC|XL|L?X?X?X?)(?:IX|IV|V?II?|III))
    """, lambda m: m != 'I')   # don't match 'I'

numeric = pattern('((?:\d{1,3}(?:\,\d{3})*|\d+)(?:\.\d+)?)')

doftw = pattern("""
    (?: Mon
        |Tues?
        |Wed(?:nes)?
        |Thurs?
        |Fri
        |Satu?r?
        |Sun
    )(?:day|\.)
    """)

month = pattern("""
    (?: Jan(?:uary|\.)
        |Febr?(?:uary|\.)
        |Mar(?:ch|\.)
        |Apr(?:il|\.)
        |May
        |Jun(?:e|\.)
        |Jul(?:y|\.)
        |Aug(?:ust|\.)
        |Sept?(?:ember|\.)
        |Oct(?:ober|\.)
        |Nov(?:ember|\.)
        |Dec(?:ember|\.)
    )
    """)

day_words = pattern("""
    (?: today
        |tomorrow
        |yesterday
        |morning
        |afternoon
        |evening
    )""")

possible_year = pattern("""
    (?: \d\d\d\d (?:\s*s)? | \'? \d\d (?:\s*?s)? )
    """)

def validate_time(hr, colon, m, ampm, tzone):
    if ampm in ('a','p','A','P') and not colon:
        return False
    if not (0 <= int(m or 0) <= 59):
        return None
    if ampm:
        if not (1 <= int(hr) <= 12):
            return None
    else:
        if not (0 <= int(hr) <= 24) or m is None:
            return None
    if not (colon or tzone or ampm):
        return None
    return True

time = pattern("""(\d\d?) \s*? (?: (\:)? \s*? (\d\d))? \s* ([ap]\.m\.?|[ap]m|[ap])?
\s* (?: \(? (GMT|EST|PST|CST)? \)? )? (?:\W|$)""", handler=validate_time)

def capitalized(tk):
    return tk.form[0].isupper() and tk.form[1:].islower()
