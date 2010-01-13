import re, sys

###
# IDEAS/TODO:
#    Nets' => Net 's
#

# Separate numbers from words.
def numbers_words(m):
    a,b = m.groups()
    if b.lower() in ['st','nd','rd','th']:
        return '%s%s' % (a,b)
    else:
        return '%s %s' % (a,b)

def wordsplit_sentence(sentence):
    # Replace repeated punctuation marks with something equivalent.  These
    # replacements also make simplifying assumptions that will become useful later
    # in this function.
    sentence = re.sub('\-\-*', '-', sentence)

    before = ''
    while before != sentence:
        before = sentence
        # Look for closing quotes
        sentence = re.sub('\'\'([^\'\w]|$)', r'" \1', sentence)
        # opening quotes
        sentence = re.sub('(^|[^\'\w\.\,\:\;\!\?])\'\'', r'\1 "', sentence)

    # Remove leading and trailing whitespace.
    sentence = sentence.strip()

    # Separate punctuation marks from each other.
    sentence = re.sub('([^\w\s\`])([^\w\s\`])', r'\1 \2', sentence)

    # Separate single quotes that don't look like apostrophes.
    sentence = re.sub('(^|\W)(\')(\w)', r'\1\2 \3', sentence)
    sentence = re.sub('(\w)(\')(\W|$)', r'\1 \2\3', sentence)

    # we want 's not ' s
    sentence = re.sub("(\w)\s*'\s*s(\W|$)", r"\1 's \2", sentence)

    # separate contractions
    sentence = re.sub('(\S)([^\w\s\`\.\,\-$])', r'\1 \2', sentence)

    sentence = re.sub('([^\w\s\`\'\.\,\-])(\S)', r'\1 \2', sentence)

    # Separate opening single quotes from everything else, except keep repeated
    # opening single quotes in pairs.
    sentence = re.sub('([^\`])(\`)', r'\1 \2', sentence)
    sentence = re.sub('(\`)([^\`])', r'\1 \2', sentence)

    before = ''
    while before != sentence:
        before = sentence
        sentence = re.sub('(^|\s)\`\`\`', r'\1\`\` \`', sentence)

    # Separate stray dashes when they don't seem to be connecting words usefully.
    sentence = re.sub('(\S)(\-)(\s|$)', r'\1 \2\3', sentence)
    sentence = re.sub('(^|\s)(\-)(\S)', r'\1\2 \3', sentence)

    # ???: always separate the dash?
    sentence = re.sub('(\-)', r' - ', sentence)

    # Separate commas from words, but not from within numbers.
    sentence = re.sub('(\S),(\s|$)', r'\1 ,\2', sentence)
    sentence = re.sub('(^|\s),(\S)', r'\1, \2', sentence)
    sentence = re.sub('(\D),(\S)', r'\1 , \2', sentence)
    sentence = re.sub('(\S),(\D)', r'\1 , \2', sentence)

    sentence = re.sub('(\d)\s*([^\W\d]+)', numbers_words, sentence)
    sentence = re.sub('([^\W\d])(\d)', r'\1 \2', sentence)

    # SMOOSH times together
    sentence = re.sub('(\d\d?)\s*:\s*(\d\d)(\W|$)', r'\1:\2\3', sentence)

    # keep things that look like abbrev, initial, honorific together
    sentence = re.sub('(^|\s)([A-Z][a-z]*)\s*\.', r'\1\2.', sentence)

    # weird thing that happens often with dates...
    sentence = re.sub('(\d),(\d{4,})(\W)', r'\1 , \2\3', sentence)

    # WARNING: I did more that word split here!
    # its that bizzare european thing...
    sentence = re.sub('(\d),(\d{2})(\W)', r'\1.\2 \3', sentence)

    # Separate words from closing punctuation (i.e., the last char in input).
    sentence = re.sub('(\w)(\.)(\W*)$', r'\1 \2 \3', sentence)

    # 1990 s -> 1990s; 90 s -> 90s
    sentence = re.sub('(\d\d\d\d|\d\d)\s*s(\s+|$)', r'\1s ', sentence)

    # ' 90 -> '90
    sentence = re.sub("'\s*(\d\d)($|\W)", r"'\1\2", sentence)

    #######
    # Tags will explode, so, as a last step,
    #  * tighten up opening tags
    sentence = re.sub('<\s*([a-zA-z_\-0-9]+?)\s*>', r'<\1>', sentence)
    #  * tighten up closing tags.
    sentence = re.sub('<\s*/\s*([a-zA-z_\-0-9]+?)\s*>', r'</\1>', sentence)
    #  * tighten-up to bracketed tags too.
    sentence = re.sub('\[\s*([A-z]+?)\s', r'[\1 ', sentence)
    #######

    return sentence


if __name__ == '__main__':
    tests = [
        'I lost 500US$ (EU800) in March 2008.',
        'I lost $500 (EU800) in March 2008.',
        'I lost 500US$ (EU800) in Mar. 18th 2008.',
        'I lost US$500.34 (EU800) in Mar. 18th 2008.',
        'I lost <NUM> 500US$ </NUM> (EU800) in Mar. 18th 2008.',
        'I lost the [NUM 50-meter] run (EU800) in Mar. 18th 2008.',
        'I lost the 55,55 in Mar. 18,2008.',
        'I lost the 55,55 in Mar . 18,2008.8.',
        'I lost the 5:30 in Mar. 18,2008.8.',
        'I lost the 5 : 30 in Mar . 18,2008.8.',
        'Dr. barry\'s . Dr . barry \'s . barry \' s .',
        'It was just [NUM .03 seconds ] back to ',
        '1990 s 1990s \' 90 \'90',
        'In 2002, 708,083 sexually transmitted infections were reported',
    ]

    for t in tests:
        print t
        print wordsplit_sentence(t)
        print


