from itertools import imap, ifilter

from arsenal.nlp.lexicon.englishwords import englishwords as dictionary

def overlap(collection):
    for w in ifilter(dictionary.__contains__, collection):
        print w

def parse(lexicon):
    return map(str.lower, imap(str.strip, lexicon.split()))


if __name__ == '__main__':

    import male
    #overlap(parse(male.male_names))

    import female
    #overlap(parse(female.female_names))

    import last
    #overlap(parse(last.last_names))

    from first_name_stats import names

