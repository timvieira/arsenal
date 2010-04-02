# -*- coding: utf-8 -*-

def remove_ligatures(text):
    for plain, funny in (('AE','\u00c6'), ('ae','\u00e6'), ('OE','\u0152'), ('oe','\u0153'),
                     ('IJ','\u0132'), ('ij','\u0133'), ('ue','\u1d6b'), ('ff','\ufb00'),
                     ('fi','\ufb01'), ('fl','\ufb02'), ('ffi','\ufb03'), ('ffl','\ufb04'),
                     ('ft','\ufb05'), ('st','\ufb06')):
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
    for plain, funny_set in (('a','áàâãäå\u0101'), ('e','éèêẽë'), ('i',"íìîĩï"), ('o','óòôõöø'),
                             ('u',"úùûũü"), ('A','ÁÀÂÃÄÅ'), ('E','ÉÈÊẼË'), ('I',"ÍÌÎĨÏ"),
                             ('O','ÓÒÔÕÖØ'), ('U',"ÚÙÛŨÜ"), ('n',"ñ"), ('c',"ç"), ('N',"Ñ"),
                             ('C',"Ç"), ('d',"Þ"), ('ss',"ß"), ('ae',"æ"), ('oe','œ')):
        for funny in funny_set:
            text = text.replace(funny, plain)
    return text

