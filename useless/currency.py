#!/usr/bin/env python

import re
import sys
from urllib2 import urlopen

def readurl(url):
    return urlopen(url).read()

def google(currencyFrom, currencyTo):
    assert currencyFrom != currencyTo
    url = 'http://www.google.com/ig/calculator?hl=en&q=1' + currencyFrom + '%3D%3F' + currencyTo
    content = readurl(url)
    try:
        [result] = re.findall(".*rhs:\s*\"(\d\.\d*)", content)
        print currencyFrom + " converted to " + currencyTo + ": %s" % float(result)
    except ValueError:
        print 'ERROR:', content

if __name__ == '__main__':
    try:
        f, t = sys.argv[1:]
    except ValueError:
        print 'usage: %s <from> <to>' % sys.argv[0]
        sys.exit(1)
    google(f,t)
