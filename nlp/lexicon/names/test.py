from itertools import imap, ifilter
from glob import glob

with file('../english-words.txt','r') as f:
    dictionary = frozenset(map(str.strip, f.xreadlines()))

def dictionary_test(collection):
    for w in ifilter(dictionary.__contains__, collection):
        print w

def parse(lexicon):
    return map(str.lower, imap(str.strip, lexicon.split()))


if __name__ == '__main__':

    import male
    #dictionary_test(parse(male.male_names))

    import female
    #dictionary_test(parse(female.female_names))

    import last
    #dictionary_test(parse(last.last_names))

    from first_name_stats import names
    #for x in names: print x

