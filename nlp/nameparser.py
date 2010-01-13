# -*- coding: utf-8 -*-
"""
A simple Python module for parsing human names into their individual components.

Components::

    * Title
    * First name
    * Middle names
    * Last names
    * Suffixes

Works for a variety of common name formats for latin-based languages. Over 
100 unit tests with example names. Should be unicode safe but it's fairly untested.

HumanName instances will pass an equals (==) test if their string representations are the same.

--------

Copyright Derek Gulbranson, May 2009 <derek73 at gmail>.
http://code.google.com/p/python-nameparser

Parser logic based on PHP nameParser.php by G. Miernicki
http://code.google.com/p/nameparser/

LGPL
http://www.opensource.org/licenses/lgpl-license.html

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser
General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License for more details.
"""

__author__ = "Derek Gulbranson"
__revision__ = "$Id: nameparser.py 20 2009-06-19 05:59:56Z derek73 $"
__version__ = "0.1.2"
__license__ = "LGPL"
__link__ = "http://code.google.com/p/python-nameparser"

TITLES = ['dr','doctor','miss','misses','mr','mister','mrs','ms','judge','sir','madam',
          'madame','AB','2ndLt','Amn','1stLt','A1C','Capt','SrA','Maj','SSgt','LtCol',
          'TSgt','Col','BrigGen','1stSgt','MajGen','SMSgt','LtGen','1stSgt','Gen','CMSgt',
          '1stSgt','CCMSgt','CMSAF','PVT','2LT','PV2','1LT','PFC','CPT','SPC','MAJ','CPL',
          'LTC','SGT','COL','SSG','BG','SFC','MG','MSG','LTG','1SGT','GEN','SGM','CSM',
          'SMA','WO1','WO2','WO3','WO4','WO5','ENS','SA','LTJG','SN','LT','PO3','LCDR',
          'PO2','CDR','PO1','CAPT','CPO','RADM(LH)','SCPO','RADM(UH)','MCPO','VADM',
          'MCPOC','ADM','MPCO-CG','CWO-2','CWO-3','CWO-4','Pvt','2ndLt','PFC','1stLt',
          'LCpl','Capt','Cpl','Maj','Sgt','LtCol','SSgt','Col','GySgt','BGen','MSgt',
          'MajGen','1stSgt','LtGen','MGySgt','Gen','SgtMaj','SgtMajMC','WO-1','CWO-2',
          'CWO-3','CWO-4','CWO-5','ENS','SA','LTJG','SN','LT','PO3','LCDR','PO2','CDR',
          'PO1','CAPT','CPO','RDML','SCPO','RADM','MCPO','VADM','MCPON','ADM','FADM',
          'WO1','CWO2','CWO3','CWO4','CWO5']
# These could be names too, but if they have period at the end they're a title
PUNC_TITLES = ['hon.']
PREFICES = ['abu','bon','ben','bin','da','dal','de','del','der','de','e','ibn','la','le','san','st','ste','van','vel','von']
SUFFICES = ['esq','esquire','jr','sr','2','i','ii','iii','iv','v','clu','chfc','cfp','md','phd']
CAPITALIZATION_EXCEPTIONS = {
    'ii': 'II',
    'iii': 'III',
    'iv': 'IV',
    'md': 'M.D.',
    'phd': 'Ph.D.'
}
CONJUNCTIONS = ['&', 'and', 'et', 'e', 'und', 'y']

ENCODING = 'utf-8'
import re
re_spaces = re.compile(r"\s+")
re_word = re.compile(r"\w+")
re_mac = re.compile(r'^(ma?c)(\w)', re.I)
re_initial = re.compile(r'^(\w\.|[A-Z])?$')

import logging
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('HumanName')

def lc(value):
    if not value:
        return ""
    return value.lower().replace('.','')

def is_not_initial(value):
    return not re_initial.match(value)

class HumanName(object):
    
    """
    Parse a person's name into individual components
    
    Usage::
    
        >>> name = HumanName("Dr. Juan Q. Xavier de la Vega III")
        >>> name.title
        'Dr.'
        >>> name.first
        'Juan'
        >>> name.middle
        'Q. Xavier'
        >>> name.last
        'de la Vega'
        >>> name.suffix
        'III'
        >>> name2 = HumanName("de la Vega, Dr. Juan Q. Xavier III")
        >>> name == name2
        True
        >>> len(name)
        5
        >>> list(name)
        ['Dr.', 'Juan', 'Q. Xavier', 'de la Vega', 'III']
        >>> name[1:-1]
        [u'Juan', u'Q. Xavier', u'de la Vega']
    
    """
    
    def __init__(self, full_name=u"", titles=TITLES, prefices=PREFICES, suffices=SUFFICES, punc_titles=PUNC_TITLES, conjunctions=CONJUNCTIONS,
      capitalization_exceptions=CAPITALIZATION_EXCEPTIONS):
        super(HumanName, self).__init__()
        self.titles = titles
        self.punc_titles = punc_titles
        self.conjunctions = conjunctions
        self.prefices = prefices
        self.suffices = suffices
        self.capitalization_exceptions = capitalization_exceptions
        self.full_name = full_name
        self.title = u""
        self.first = u""
        self.suffixes = []
        self.middle_names = []
        self.last_names = []
        self.unparsable = False
        self.count = 0
        self.members = ['title','first','middle','last','suffix']
        if self.full_name:
            self.parse_full_name()
    
    def __iter__(self):
        return self
    
    def __len__(self):
        l = 0
        for x in self:
            l += 1
        return l
    
    def __eq__(self, other):
        """HumanName instances are equal to other objects whose lower case unicode representations are the same"""
        return unicode(self).lower() == unicode(other).lower()
    
    def __ne__(self, other):
        return not unicode(self).lower() == unicode(other).lower()
    
    def __getitem__(self, key):
        return [getattr(self, x) for x in self.members[key]]
    
    def next(self):
        if self.count >= len(self.members):
            self.count = 0
            raise StopIteration
        else:
            c = self.count
            self.count = c + 1
            return getattr(self, self.members[c]) or self.next()

    def __unicode__(self):
        return u" ".join(self)
    
    def __str__(self):
        return self.__unicode__().encode('utf-8')
    
    def __repr__(self):
        if self.unparsable:
            return u"<%(class)s : [ Unparsable ] >" % {'class': self.__class__.__name__,}
        return u"<%(class)s : [\n\tTitle: '%(title)s' \n\tFirst: '%(first)s' \n\tMiddle: '%(middle)s' \n\tLast: '%(last)s' \n\tSuffix: '%(suffix)s'\n]>" % {
            'class': self.__class__.__name__,
            'title': self.title,
            'first': self.first,
            'middle': self.middle,
            'last': self.last,
            'suffix': self.suffix,
        }
    
    @property
    def middle(self):
        return u" ".join(self.middle_names)
    
    @property
    def last(self):
        return u" ".join(self.last_names)
    
    @property
    def suffix(self):
        return u", ".join(self.suffixes)
    
    def is_conjunction(self, piece):
        return lc(piece) in self.conjunctions and is_not_initial(piece)
    
    def is_prefix(self, piece):
        return lc(piece) in self.prefices and is_not_initial(piece)
    
    def parse_full_name(self):
        if not self.full_name:
            raise AttributeError("Missing full_name")
        
        if not isinstance(self.full_name, unicode):
            self.full_name = unicode(self.full_name, ENCODING)
        # collapse multiple spaces
        self.full_name = re.sub(re_spaces, u" ", self.full_name.strip() )
        
        # reset values
        self.title = u""
        self.first = u""
        self.suffixes = []
        self.middle_names = []
        self.last_names = []
        self.unparsable = False
        
        # break up full_name by commas
        parts = [x.strip() for x in self.full_name.split(",")]
        
        log.debug(u"full_name: " + self.full_name)
        log.debug(u"parts: " + unicode(parts))
        
        pieces = []
        if len(parts) == 1:
            
            # no commas, title first middle middle middle last suffix
            
            for part in parts:
                names = part.split(' ')
                for name in names:
                    name.replace(',','').strip()
                    pieces.append(name)
            
            log.debug(u"pieces: " + unicode(pieces))
            
            for i, piece in enumerate(pieces):
                try:
                    next = pieces[i + 1]
                except IndexError:
                    next = None

                try:
                    prev = pieces[i - 1]
                except IndexError:
                    prev = None
                
                if lc(piece) in self.titles:
                    self.title = piece
                    continue
                if piece.lower() in self.punc_titles:
                    self.title = piece
                    continue
                if not self.first:
                    self.first = piece.replace(".","")
                    continue
                if (i == len(pieces) - 2) and (lc(next) in self.suffices):
                    self.last_names.append(piece)
                    self.suffixes.append(next)
                    break
                if self.is_prefix(piece):
                    self.last_names.append(piece)
                    continue
                if self.is_conjunction(piece) and i < len(pieces) / 2:
                    self.first += ' ' + piece
                    continue
                if self.is_conjunction(prev) and (i-1) < len(pieces) / 2:
                    self.first += ' ' + piece
                    continue
                if self.is_conjunction(piece) or self.is_conjunction(next):
                    self.last_names.append(piece)
                    continue
                if i == len(pieces) - 1:
                    self.last_names.append(piece)
                    continue
                self.middle_names.append(piece)
        else:
            if lc(parts[1]) in self.suffices:
                
                # title first middle last, suffix [, suffix]
                
                names = parts[0].split(' ')
                for name in names:
                    name.replace(',','').strip()
                    pieces.append(name)
                
                log.debug(u"pieces: " + unicode(pieces))
                
                self.suffixes += parts[1:]
                
                for i, piece in enumerate(pieces):
                    try:
                        next = pieces[i + 1]
                    except IndexError:
                        next = None

                    if lc(piece) in self.titles:
                        self.title = piece
                        continue
                    if piece.lower() in self.punc_titles:
                        self.title = piece
                        continue
                    if not self.first:
                        self.first = piece.replace(".","")
                        continue
                    if i == (len(pieces) -1) and self.is_prefix(piece):
                        self.last_names.append(piece + " " + next)
                        break
                    if self.is_prefix(piece):
                        self.last_names.append(piece)
                        continue
                    if self.is_conjunction(piece) or self.is_conjunction(next):
                        self.last_names.append(piece)
                        continue
                    if i == len(pieces) - 1:
                        self.last_names.append(piece)
                        continue
                    self.middle_names.append(piece)
            else:
                
                # last, title first middles[,] suffix [,suffix]
                
                names = parts[1].split(' ')
                for name in names:
                    name.replace(',','').strip()
                    pieces.append(name)
                
                log.debug(u"pieces: " + unicode(pieces))
                
                self.last_names.append(parts[0])
                for i, piece in enumerate(pieces):
                    try:
                        next = pieces[i + 1]
                    except IndexError:
                        next = None
                    
                    if lc(piece) in self.titles:
                        self.title = piece
                        continue
                    if piece.lower() in self.punc_titles:
                        self.title = piece
                        continue
                    if not self.first:
                        self.first = piece.replace(".","")
                        continue
                    if lc(piece) in self.suffices:
                        self.suffixes.append(piece)
                        continue
                    self.middle_names.append(piece)
                try:
                    if parts[2]:
                        self.suffixes += parts[2:]
                except IndexError:
                    pass
                
        if not self.first and len(self.middle_names) < 1 and len(self.last_names) < 1:
            self.unparsable = True
            log.error(u"Unparsable full_name: " + self.full_name)
    
    def cap_word(self, word):
        if self.is_prefix(word) or self.is_conjunction(word):
            return lc(word)
        if word in self.capitalization_exceptions:
            return self.capitalization_exceptions[word]
        mac_match = re_mac.match(word)
        if mac_match:
            def cap_after_mac(m):
                return m.group(1).capitalize() + m.group(2).capitalize()
            return re_mac.sub(cap_after_mac, word)
        else:
            return word.capitalize()

    def cap_piece(self, piece):
        if not piece:
            return ""
        replacement = lambda m: self.cap_word(m.group(0))
        return re.sub(re_word, replacement, piece)

    def capitalize(self):
        name = unicode(self)
        if not (name == name.upper() or name == name.lower()):
            return
        self.title = self.cap_piece(self.title)
        self.first = self.cap_piece(self.first)
        self.middle_names = self.cap_piece(self.middle).split(' ')
        self.last_names = self.cap_piece(self.last).split(' ')
        self.suffixes = self.cap_piece(self.suffix).split(' ')




#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run this file to run the tests, e.g "python tests.py" or "./tests.py".
Post a ticket and/or patch/diff of this file for names that fail and I will try to fix it.
http://code.google.com/p/python-nameparser/issues/entry
"""

from nameparser import HumanName
import unittest
class HumanNameTests(unittest.TestCase):
    
    def assertMatches(self, actual, expected, parsed):
        """assertEquals with a better message"""
        try:
            self.assertEquals(actual, expected, u"'%s' != '%s' for '%s'\n%s" % (
                    actual, 
                    expected, 
                    parsed.full_name, 
                    parsed
                )
            )
        except UnicodeDecodeError:
            self.assertEquals(actual, expected )
    
    def test_utf8(self):
        parsed = HumanName("de la Véña, Jüan")
        self.assertMatches(parsed.first,u"Jüan", parsed)
        self.assertMatches(parsed.last, u"de la Véña", parsed)
    
    def test_unicode(self):
        parsed = HumanName(u"de la Véña, Jüan")
        self.assertMatches(parsed.first,u"Jüan", parsed)
        self.assertMatches(parsed.last, u"de la Véña", parsed)
    
    def test_len(self):
        parsed = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.assertMatches(len(parsed), 5, parsed)
        parsed = HumanName("John Doe")
        self.assertMatches(len(parsed), 2, parsed)
    
    def test_comparison(self):
        parsed1 = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        parsed2 = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.assert_(parsed1 == parsed2)
        self.assert_(not parsed1 is parsed2)
        self.assert_(parsed1 == "Dr. John P. Doe-Ray CLU, CFP, LUTC")
        parsed1 = HumanName("Doe, Dr. John P., CLU, CFP, LUTC")
        parsed2 = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.assert_(not parsed1 == parsed2)
        self.assert_(not parsed1 == 0)
        self.assert_(not parsed1 == "test")
        self.assert_(not parsed1 == ["test"])
        self.assert_(not parsed1 == {"test":parsed2})
    
    def test_comparison_case_insensitive(self):
        parsed1 = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        parsed2 = HumanName("dr. john p. doe-Ray, CLU, CFP, LUTC")
        self.assert_(parsed1 == parsed2)
        self.assert_(not parsed1 is parsed2)
        self.assert_(parsed1 == "Dr. John P. Doe-ray clu, CFP, LUTC")
    
    def test_slice(self):
        parsed = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.assertMatches(list(parsed), [u'Dr.', u'John', u'P.', u'Doe-Ray', u'CLU, CFP, LUTC'], parsed)
        self.assertMatches(parsed[1:], [u'John', u'P.', u'Doe-Ray', u'CLU, CFP, LUTC'], parsed)
        self.assertMatches(parsed[1:-1], [u'John', u'P.', u'Doe-Ray'], parsed)
    
    def test1(self):
        parsed = HumanName("John Doe")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
    
    def test2(self):
        parsed = HumanName("John Doe, Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test3(self):
        parsed = HumanName("John Doe III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test4(self):
        parsed = HumanName("Doe, John")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
    
    def test5(self):
        parsed = HumanName("Doe, John, Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test6(self):
        parsed = HumanName("Doe, John III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test7(self):
        parsed = HumanName("John A. Doe")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
    
    def test8(self):
        parsed = HumanName("John A. Doe, Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test9(self):
        parsed = HumanName("John A. Doe III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test10(self):
        parsed = HumanName("Doe, John. A.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
    
    def test11(self):
        parsed = HumanName("Doe, John. A., Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test12(self):
        parsed = HumanName("Doe, John. A., III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test13(self):
        parsed = HumanName("John A. Kenneth Doe")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
    
    def test14(self):
        parsed = HumanName("John A. Kenneth Doe, Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test15(self):
        parsed = HumanName("John A. Kenneth Doe III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test16(self):
        parsed = HumanName("Doe, John. A. Kenneth")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
    
    def test17(self):
        parsed = HumanName("Doe, John. A. Kenneth, Jr.")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test18(self):
        parsed = HumanName("Doe, John. A. Kenneth III")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test19(self):
        parsed = HumanName("Dr. John Doe")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
    
    def test20(self):
        parsed = HumanName("Dr. John Doe, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test21(self):
        parsed = HumanName("Dr. John Doe III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test22(self):
        parsed = HumanName("Doe, Dr. John")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
    
    def test23(self):
        parsed = HumanName("Doe, Dr. John, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test24(self):
        parsed = HumanName("Doe, Dr. John III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test25(self):
        parsed = HumanName("Dr. John A. Doe")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
    
    def test26(self):
        parsed = HumanName("Dr. John A. Doe, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test27(self):
        parsed = HumanName("Dr. John A. Doe III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test28(self):
        parsed = HumanName("Doe, Dr. John A.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
    
    def test29(self):
        parsed = HumanName("Doe, Dr. John A. Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test30(self):
        parsed = HumanName("Doe, Dr. John A. III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test31(self):
        parsed = HumanName("Dr. John A. Kenneth Doe")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
    
    def test32(self):
        parsed = HumanName("Dr. John A. Kenneth Doe, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test33(self):
        parsed = HumanName("Al Arnold Gore, Jr.")
        self.assertMatches(parsed.middle,"Arnold", parsed)
        self.assertMatches(parsed.first,"Al", parsed)
        self.assertMatches(parsed.last,"Gore", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test34(self):
        parsed = HumanName("Dr. John A. Kenneth Doe III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test35(self):
        parsed = HumanName("Doe, Dr. John A. Kenneth")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
    
    def test36(self):
        parsed = HumanName("Doe, Dr. John A. Kenneth Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test37(self):
        parsed = HumanName("Doe, Dr. John A. Kenneth III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"A. Kenneth", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test38(self):
        parsed = HumanName("Juan de la Vega")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test39(self):
        parsed = HumanName("Juan de la Vega, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test40(self):
        parsed = HumanName("Juan de la Vega III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test41(self):
        parsed = HumanName("de la Vega, Juan")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test42(self):
        parsed = HumanName("de la Vega, Juan, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test43(self):
        parsed = HumanName("de la Vega, Juan III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test44(self):
        parsed = HumanName("Juan Velasquez y Garcia")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test45(self):
        parsed = HumanName("Juan Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test46(self):
        parsed = HumanName("Juan Velasquez y Garcia III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test47(self):
        parsed = HumanName("Velasquez y Garcia, Juan")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test48(self):
        parsed = HumanName("Velasquez y Garcia, Juan, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test49(self):
        parsed = HumanName("Velasquez y Garcia, Juan III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test50(self):
        parsed = HumanName("Dr. Juan de la Vega")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test51(self):
        parsed = HumanName("Dr. Juan de la Vega, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test52(self):
        parsed = HumanName("Dr. Juan de la Vega III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test53(self):
        parsed = HumanName("de la Vega, Dr. Juan")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test54(self):
        parsed = HumanName("de la Vega, Dr. Juan, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test55(self):
        parsed = HumanName("de la Vega, Dr. Juan III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test56(self):
        parsed = HumanName("Dr. Juan Velasquez y Garcia")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test57(self):
        parsed = HumanName("Dr. Juan Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test58(self):
        parsed = HumanName("Dr. Juan Velasquez y Garcia III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test59(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test60(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test61(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan III")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test62(self):
        parsed = HumanName("Juan Q. de la Vega")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test63(self):
        parsed = HumanName("Juan Q. de la Vega, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test64(self):
        parsed = HumanName("Juan Q. de la Vega III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test65(self):
        parsed = HumanName("de la Vega, Juan Q.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test66(self):
        parsed = HumanName("de la Vega, Juan Q., Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test67(self):
        parsed = HumanName("de la Vega, Juan Q. III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test68(self):
        parsed = HumanName("Juan Q. Velasquez y Garcia")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test69(self):
        parsed = HumanName("Juan Q. Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test70(self):
        parsed = HumanName("Juan Q. Velasquez y Garcia III")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test71(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q.")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test72(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q., Jr.")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test73(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q. III")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test74(self):
        parsed = HumanName("Dr. Juan Q. de la Vega")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test75(self):
        parsed = HumanName("Dr. Juan Q. de la Vega, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test76(self):
        parsed = HumanName("Dr. Juan Q. de la Vega III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test77(self):
        parsed = HumanName("de la Vega, Dr. Juan Q.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
    
    def test78(self):
        parsed = HumanName("de la Vega, Dr. Juan Q., Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
    
    def test79(self):
        parsed = HumanName("de la Vega, Dr. Juan Q. III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last, u"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
    
    def test80(self):
        parsed = HumanName("Dr. Juan Q. Velasquez y Garcia")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test81(self):
        parsed = HumanName("Dr. Juan Q. Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test82(self):
        parsed = HumanName("Dr. Juan Q. Velasquez y Garcia III")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test83(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q.")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test84(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q., Jr.")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test85(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q. III")
        self.assertMatches(parsed.middle,"Q.", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test86(self):
        parsed = HumanName("Juan Q. Xavier de la Vega")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test87(self):
        parsed = HumanName("Juan Q. Xavier de la Vega, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test88(self):
        parsed = HumanName("Juan Q. Xavier de la Vega III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test89(self):
        parsed = HumanName("de la Vega, Juan Q. Xavier")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test90(self):
        parsed = HumanName("de la Vega, Juan Q. Xavier, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test91(self):
        parsed = HumanName("de la Vega, Juan Q. Xavier III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test92(self):
        parsed = HumanName("Dr. Juan Q. Xavier de la Vega")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test93(self):
        parsed = HumanName("Dr. Juan Q. Xavier de la Vega, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test94(self):
        parsed = HumanName("Dr. Juan Q. Xavier de la Vega III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test95(self):
        parsed = HumanName("de la Vega, Dr. Juan Q. Xavier")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
    
    def test96(self):
        parsed = HumanName("de la Vega, Dr. Juan Q. Xavier, Jr.")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test97(self):
        parsed = HumanName("de la Vega, Dr. Juan Q. Xavier III")
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"de la Vega", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test98(self):
        parsed = HumanName("Juan Q. Xavier Velasquez y Garcia")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test99(self):
        parsed = HumanName("Juan Q. Xavier Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test100(self):
        parsed = HumanName("Juan Q. Xavier Velasquez y Garcia III")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test101(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q. Xavier")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test102(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q. Xavier, Jr.")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test103(self):
        parsed = HumanName("Velasquez y Garcia, Juan Q. Xavier III")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test104(self):
        parsed = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test105(self):
        parsed = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia, Jr.")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test106(self):
        parsed = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia III")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test107(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
    
    def test108(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier, Jr.")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"Jr.", parsed)
    
    def test109(self):
        parsed = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier III")
        self.assertMatches(parsed.middle,"Q. Xavier", parsed)
        self.assertMatches(parsed.first,"Juan", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.last,"Velasquez y Garcia", parsed)
        self.assertMatches(parsed.suffix,"III", parsed)
    
    def test110(self):
        parsed = HumanName("John Doe, CLU, CFP, LUTC")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"CLU, CFP, LUTC", parsed)
    
    def test111(self):
        parsed = HumanName("John P. Doe, CLU, CFP, LUTC")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.middle,"P.", parsed)
        self.assertMatches(parsed.last,"Doe", parsed)
        self.assertMatches(parsed.suffix,"CLU, CFP, LUTC", parsed)
    
    def test112(self):
        parsed = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.middle,"P.", parsed)
        self.assertMatches(parsed.last,"Doe-Ray", parsed)
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.suffix,"CLU, CFP, LUTC", parsed)
    
    def test113(self):
        parsed = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.assertMatches(parsed.title,"Dr.", parsed)
        self.assertMatches(parsed.middle,"P.", parsed)
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"Doe-Ray", parsed)
        self.assertMatches(parsed.suffix,"CLU, CFP, LUTC", parsed)
    
    def test114(self):
        parsed = HumanName("Hon Oladapo")
        self.assertMatches(parsed.first,"Hon", parsed)
        self.assertMatches(parsed.last,"Oladapo", parsed)
    
    def test115(self):
        parsed = HumanName("Hon. Barrington P. Doe-Ray, Jr.")
        self.assertMatches(parsed.title,"Hon.", parsed)
        self.assertMatches(parsed.middle,"P.", parsed)
        self.assertMatches(parsed.first,"Barrington", parsed)
        self.assertMatches(parsed.last,"Doe-Ray", parsed)
    
    def test116(self):
        parsed = HumanName("Doe-Ray, Hon. Barrington P. Jr., CFP, LUTC")
        self.assertMatches(parsed.title,"Hon.", parsed)
        self.assertMatches(parsed.middle,"P.", parsed)
        self.assertMatches(parsed.first,"Barrington", parsed)
        self.assertMatches(parsed.last,"Doe-Ray", parsed)
        self.assertMatches(parsed.suffix,"Jr., CFP, LUTC", parsed)
    
    # Last name with conjunction
    def test117(self):
        parsed = HumanName('Jose Aznar y Lopez')
        self.assertMatches(parsed.first,"Jose", parsed)
        self.assertMatches(parsed.last,"Aznar y Lopez", parsed)
    
    # Potential conjunction/prefix treated as initial (because uppercase)
    def test118(self):
        parsed = HumanName('John E Smith')
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.middle,"E", parsed)
        self.assertMatches(parsed.last,"Smith", parsed)
    
    # The prefix "e"
    def test119(self):
        parsed = HumanName('John e Smith')
        self.assertMatches(parsed.first,"John", parsed)
        self.assertMatches(parsed.last,"e Smith", parsed)
    
    # Couple's name
    def test120(self):
        parsed = HumanName('John and Jane Smith')
        self.assertMatches(parsed.first,"John and Jane", parsed)
        self.assertMatches(parsed.last,"Smith", parsed)
    
    # Capitalization, including conjunction and exception for 'III'
    def test121(self):
        parsed = HumanName('juan q. xavier velasquez y garcia iii')
        parsed.capitalize()
        self.assertMatches(str(parsed), 'Juan Q. Xavier Velasquez y Garcia III', parsed)
    
    # Capitalization with M(a)c and hyphenated names
    def test122(self):
        parsed = HumanName('donovan mcnabb-smith')
        parsed.capitalize()
        self.assertMatches(str(parsed), 'Donovan McNabb-Smith', parsed)
    
    # Leaving already-capitalized names alone
    def test123(self):
        parsed = HumanName('Shirley Maclaine')
        parsed.capitalize()
        self.assertMatches(str(parsed), 'Shirley Maclaine', parsed)

TEST_NAMES = (
    "John Doe",
    "John Doe, Jr.",
    "John Doe III",
    "Doe, John",
    "Doe, John, Jr.",
    "Doe, John III",
    "John A. Doe",
    "John A. Doe, Jr.",
    "John A. Doe III",
    "Doe, John. A.",
    "Doe, John. A., Jr.",
    "Doe, John. A. III",
    "John A. Kenneth Doe",
    "John A. Kenneth Doe, Jr.",
    "John A. Kenneth Doe III",
    "Doe, John. A. Kenneth",
    "Doe, John. A. Kenneth, Jr.",
    "Doe, John. A. Kenneth III",
    "Dr. John Doe",
    "Dr. John Doe, Jr.",
    "Dr. John Doe III",
    "Doe, Dr. John",
    "Doe, Dr. John, Jr.",
    "Doe, Dr. John III",
    "Dr. John A. Doe",
    "Dr. John A. Doe, Jr.",
    "Dr. John A. Doe III",
    "Doe, Dr. John A.",
    "Doe, Dr. John A. Jr.",
    "Doe, Dr. John A. III",
    "Dr. John A. Kenneth Doe",
    "Dr. John A. Kenneth Doe, Jr.",
    "Dr. John A. Kenneth Doe III",
    "Doe, Dr. John A. Kenneth",
    "Doe, Dr. John A. Kenneth Jr.",
    "Doe, Dr. John A. Kenneth III",
    "Juan de la Vega",
    "Juan de la Vega, Jr.",
    "Juan de la Vega III",
    "de la Vega, Juan",
    "de la Vega, Juan, Jr.",
    "de la Vega, Juan III",
    "Juan Velasquez y Garcia",
    "Juan Velasquez y Garcia, Jr.",
    "Juan Velasquez y Garcia III",
    "Velasquez y Garcia, Juan",
    "Velasquez y Garcia, Juan, Jr.",
    "Velasquez y Garcia, Juan III",
    "Dr. Juan de la Vega",
    "Dr. Juan de la Vega, Jr.",
    "Dr. Juan de la Vega III",
    "de la Vega, Dr. Juan",
    "de la Vega, Dr. Juan, Jr.",
    "de la Vega, Dr. Juan III",
    "Dr. Juan Velasquez y Garcia",
    "Dr. Juan Velasquez y Garcia, Jr.",
    "Dr. Juan Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan",
    "Velasquez y Garcia, Dr. Juan, Jr.",
    "Velasquez y Garcia, Dr. Juan III",
    "Juan Q. de la Vega",
    "Juan Q. de la Vega, Jr.",
    "Juan Q. de la Vega III",
    "de la Vega, Juan Q.",
    "de la Vega, Juan Q., Jr.",
    "de la Vega, Juan Q. III",
    "Juan Q. Velasquez y Garcia",
    "Juan Q. Velasquez y Garcia, Jr.",
    "Juan Q. Velasquez y Garcia III",
    "Velasquez y Garcia, Juan Q.",
    "Velasquez y Garcia, Juan Q., Jr.",
    "Velasquez y Garcia, Juan Q. III",
    "Dr. Juan Q. de la Vega",
    "Dr. Juan Q. de la Vega, Jr.",
    "Dr. Juan Q. de la Vega III",
    "de la Vega, Dr. Juan Q.",
    "de la Vega, Dr. Juan Q., Jr.",
    "de la Vega, Dr. Juan Q. III",
    "Dr. Juan Q. Velasquez y Garcia",
    "Dr. Juan Q. Velasquez y Garcia, Jr.",
    "Dr. Juan Q. Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan Q.",
    "Velasquez y Garcia, Dr. Juan Q., Jr.",
    "Velasquez y Garcia, Dr. Juan Q. III",
    "Juan Q. Xavier de la Vega",
    "Juan Q. Xavier de la Vega, Jr.",
    "Juan Q. Xavier de la Vega III",
    "de la Vega, Juan Q. Xavier",
    "de la Vega, Juan Q. Xavier, Jr.",
    "de la Vega, Juan Q. Xavier III",
    "Juan Q. Xavier Velasquez y Garcia",
    "Juan Q. Xavier Velasquez y Garcia, Jr.",
    "Juan Q. Xavier Velasquez y Garcia III",
    "Velasquez y Garcia, Juan Q. Xavier",
    "Velasquez y Garcia, Juan Q. Xavier, Jr.",
    "Velasquez y Garcia, Juan Q. Xavier III",
    "Dr. Juan Q. Xavier de la Vega",
    "Dr. Juan Q. Xavier de la Vega, Jr.",
    "Dr. Juan Q. Xavier de la Vega III",
    "de la Vega, Dr. Juan Q. Xavier",
    "de la Vega, Dr. Juan Q. Xavier, Jr.",
    "de la Vega, Dr. Juan Q. Xavier III",
    "Dr. Juan Q. Xavier Velasquez y Garcia",
    "Dr. Juan Q. Xavier Velasquez y Garcia, Jr.",
    "Dr. Juan Q. Xavier Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan Q. Xavier",
    "Velasquez y Garcia, Dr. Juan Q. Xavier, Jr.",
    "Velasquez y Garcia, Dr. Juan Q. Xavier III",
    "John Doe, CLU, CFP, LUTC",
    "John P. Doe, CLU, CFP, LUTC",
    "Dr. John P. Doe-Ray, CLU, CFP, LUTC",
    "Doe-Ray, Dr. John P., CLU, CFP, LUTC",
    "Hon. Barrington P. Doe-Ray, Jr.",
    "Doe-Ray, Hon. Barrington P. Jr.",
    "Doe-Ray, Hon. Barrington P. Jr., CFP, LUTC",
    "Hon Oladapo",
    "Jose Aznar y Lopez",
    "John E Smith",
    "John e Smith",
    "John and Jane Smith"
)

if __name__ == '__main__':
    for name in TEST_NAMES:
        parsed = HumanName(name)
        print unicode(name)
        print unicode(parsed)
        print repr(parsed)
        print "\n-------------------------------------------\n"
    unittest.main()

