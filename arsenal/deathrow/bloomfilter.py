#!/usr/bin/python
"""
Bloom filters in Python, using SHA-1 and Python longs.

My first attempt stored the whole filter in a single arbitrary-size integer,
but for some reason that was 100x slower than storing it in a bunch of 256-bit
integers.
"""

from hashlib import sha1

def nbits_required(n):
    """ Calculate the number of bits required to represent any integer in [0, n). """
    n -= 1
    rv = 0
    while n:
        n >>= 1
        rv += 1
    return rv

class Bloom:
    """ Bloom filter: compact hash table for membership tests with false pos. """

    def __init__(self, size, nhashes, bucketbits=256):
        """
        size: number of bits.  Should be a power of 2.
        nhashes: number of separate hashes to use.

        Making nhashes larger will make it slower.  There are also tradeoffs
        between size, performance, and false-positive rate, which you can look
        up elsewhere.

        default bits per bucket is 256 to cut down on pickle overhead
        """
        self.bucketbits = bucketbits
        self.filter = [0L] * int((size + bucketbits - 1) / bucketbits)
        self.size = size
        self.nhashes = nhashes
        self.hashbits = nbits_required(size)
        assert self.hashbits * nhashes <= 160  # 160's all we get with SHA1

    def add(self, astr):
        """ Add a string to the membership of the filter. """
        for offset in self._hashes(astr):
            bucket, bit = divmod(offset, self.bucketbits)
            self.filter[bucket] |= (1L << bit)

    def __contains__(self, astr):
        """ Returns true if the string is in the filter or it feels like it. """
        for offset in self._hashes(astr):
            bucket, bit = divmod(offset, self.bucketbits)
            if not self.filter[bucket] & (1L << bit): return 0
        return 1

    def _hashes(self, astr):
        """ The hashes of a particular string. """
        digest = sha1(astr).digest()
        # is there no better way to convert a byte string into a long?!
        hashlong = 0L
        for ch in digest:
            hashlong = (hashlong << 8) | ord(ch)
        rv = []
        mask = (1L << self.hashbits) - 1
        for ii in range(self.nhashes):
            # Note that this will give substantially nonuniform results if
            # self.size is not a power of 2, in order to avoid wasting hash
            # bits or doing long division:
            rv.append((hashlong & mask) % self.size)
            hashlong >>= self.hashbits
        return rv

def test_bloom():
    """ Very basic sanity test for Bloom filter implementation. """
    print 'runnning test_bloom...'

    def ok(a, b): assert a == b, (a, b)
    ok(map(nbits_required, range(1, 10)), [0, 1, 2, 2, 3, 3, 3, 3, 4])
    ok(nbits_required(131072), 17)
    ok(nbits_required(131073), 18)

    b = Bloom(1024, 5)
    assert 'asdf' not in b
    assert 'fdsa' not in b
    b.add('asdf')
    assert 'asdf' in b
    assert 'fdsa' not in b

    # false positives (depends on hash function):
    x = Bloom(8, 3)
    x.add('asdf') # about a 5% chance of false positives
    assert 'asdf' in x
    assert 'fdsa' not in x
    ok(filter(x.__contains__, ['foo%d' % ii for ii in range(25)]), ['foo22'])

    print 'pass.'


def misspellings(passage, WORDS):

    import re, cPickle, sys
    try:
        bf = cPickle.load(file('dict.pkl', 'rb'))
    except IOError:
        # /usr/share/dict/words has 234936 words on this Mac and is 2.4 megs
        print "reading dictionary..."
        words = file(WORDS)
        # 2^21 bits, 8.9 per word, would give us 1.5% false positives with 5
        # hashes or 1.7% with 6, so we use 4194304 = 2^22 bits, or 17.8 per
        # word, for 0.09% false positives; that's still only half a mebibyte,
        # although pickle overhead pushes it up to 559K, 22% of the dictionary.
        bf = Bloom(4194304, 5)  
        for line in words: 
            #bf.add(line[:-1].lower())
            bf.add(line.strip().lower().split('/')[0])

        print 'done reading dictionary'
        try:
            cPickle.dump(bf, file('dict.pkl', 'wb'), 2)
        except:
            pass

    def candidates(word):
        """ Words you might find in the dictionary in English. """
        yield word
        for suffix in ['s', 'ing', 'ed', 'es', 'er', 's', 'ly']:
            if word.endswith(suffix):
                yield word[:-len(suffix)]
        for suffix, repl in [('ed', 'e'), ('er', 'e'), ('ing', 'e'), ('ies', 'y'), ('ied', 'y')]:
            if word.endswith(suffix):
                yield word[:-len(suffix)] + repl

    for word in passage:
        # we drop the "'" because our dictionary has "didnt" but not "didn't"
        for chance in candidates(word.replace("'", '').lower()):
            if chance in bf: break
        else:
            print 'typo: %r' % word
            bf.add(word)
    sys.stdout.write('\n')

if __name__ == '__main__':
    test_bloom()

    import sys
    if sys.platform.startswith('win') or sys.platform == 'nt':
        dic = 'C:/Program Files/Mozilla Firefox/dictionaries/en-US.dic'
    else:
        dic = '/usr/share/dict/words'

    sentence = 'You might have a typo in yur codez'
    print 'sentence:', sentence
    misspellings(sentence.split(), dic)

