#!/usr/bin/env python

import re
import sys
from urllib2 import urlopen

def readurl(url):
    return urlopen(url).read()

## def oanda(fromcurr, tocurr):
##     # http://www.oanda.com/currency/historical-rates?expr2=EUR&exch2=USD&format=ASCII&date1=01/13/11&date=01/19/11&lang=en&result=1
##     fromdate = '01/13/11'
##     todate = '01/19/11'
##     url = 'http://www.oanda.com/currency/historical-rates?lang=en&result=1&format=ASCII'
##     url += '&exch2=%s&expr2=%s' % (fromcurr, tocurr)
##     url += '&date1=%s&date=%s' % (fromdate, todate)
##     content = readurll(url)
##     pre = re.findall('<pre.*>([\w\W]*?)</pre>', content, re.IGNORECASE)
##     assert len(pre) == 1
##     print [(a, float(b)) for (a,b) in (x.split() for x in pre[0].strip().split('\n'))]

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
