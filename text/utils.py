#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from text import markup


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
    except UnicodeDecodeError, e:
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


LIGATURES_MAP = dict([
    (u'ﬀ', 'ff'),
    (u'ﬁ', 'fi', ),
    (u'—', '--'),
    (u'ﬃ', 'ffi'),
    (u'ﬂ', 'fl'),

    (u'“', '"'),
    (u'”', '"'),
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
])

LIGATURES = re.compile('(%s)' % '|'.join(LIGATURES_MAP.keys()))

def remove_ligatures(text):
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





#   ' '    &#160;  &nbsp;
XXX = u"""
    ™ &#8482;
    € &euro;
    !  &#33;
    "  &#34;   &quot;
    #  &#35;
    $  &#36;
    %  &#37;
    &  &#38;   &amp;
    '  &#39;
    (  &#40;
    )  &#41;
    *  &#42;
    +  &#43;
    ,  &#44;
    -  &#45;
    .  &#46;
    /  &#47;
    0  &#48;
    1  &#49;
    2  &#50;
    3  &#51;
    4  &#52;
    5  &#53;
    6  &#54;
    7  &#55;
    8  &#56;
    9  &#57;
    :  &#58;
    ;  &#59;
    <  &#60;   &lt;
    =  &#61;
    >  &#62;   &gt;
    ?  &#63;
    @  &#64;
    A  &#65;
    B  &#66;
    C  &#67;
    D  &#68;
    E  &#69;
    F  &#70;
    G  &#71;
    H  &#72;
    I  &#73;
    J  &#74;
    K  &#75;
    L  &#76;
    M  &#77;
    N  &#78;
    O  &#79;
    P  &#80;
    Q  &#81;
    R  &#82;
    S  &#83;
    T  &#84;
    U  &#85;
    V  &#86;
    W  &#87;
    X  &#88;
    Y  &#89;
    Z  &#90;
    [  &#91;
    \  &#92;
    ]  &#93;
    ^  &#94;
    _  &#95;
    `  &#96;
    a  &#97;
    b  &#98;
    c  &#99;
    d  &#100;
    e  &#101;
    f  &#102;
    g  &#103;
    h  &#104;
    i  &#105;
    j  &#106;
    k  &#107;
    l  &#108;
    m  &#109;
    n  &#110;
    o  &#111;
    p  &#112;
    q  &#113;
    r  &#114;
    s  &#115;
    t  &#116;
    u  &#117;
    v  &#118;
    w  &#119;
    x  &#120;
    y  &#121;
    z  &#122;
    {  &#123;
    |  &#124;
    }  &#125;
    ~  &#126;
    ¡  &#161;  &iexcl;
    ¢  &#162;  &cent;
    £  &#163;  &pound;
    ¤  &#164;  &curren;
    ¥  &#165;  &yen;
    ¦  &#166;  &brvbar;
    §  &#167;  &sect;
    ¨  &#168;  &uml;
    ©  &#169;  &copy;
    ª  &#170;  &ordf;
    «  &#171;
    ¬  &#172;  &not;
    ®  &#174;  &reg;
    ¯  &#175;  &macr;
    °  &#176;  &deg;
    ±  &#177;  &plusmn;
    ²  &#178;  &sup2;
    ³  &#179;  &sup3;
    ´  &#180;  &acute;
    µ  &#181;  &micro;
    ¶  &#182;  &para;
    ·  &#183;  &middot;
    ¸  &#184;  &cedil;
    ¹  &#185;  &sup1;
    º  &#186;  &ordm;
    »  &#187;  &raquo;
    ¼  &#188;  &frac14;
    ½  &#189;  &frac12;
    ¾  &#190;  &frac34;
    ¿  &#191;  &iquest;
    À  &#192;  &Agrave;
    Á  &#193;  &Aacute;
    Â  &#194;  &Acirc;
    Ã  &#195;  &Atilde;
    Ä  &#196;  &Auml;
    Å  &#197;  &Aring;
    Æ  &#198;  &AElig;
    Ç  &#199;  &Ccedil;
    È  &#200;  &Egrave;
    É  &#201;  &Eacute;
    Ê  &#202;  &Ecirc;
    Ë  &#203;  &Euml;
    Ì  &#204;  &Igrave;
    Í  &#205;  &Iacute;
    Î  &#206;  &Icirc;
    Ï  &#207;  &Iuml;
    Ð  &#208;  &ETH;
    Ñ  &#209;  &Ntilde;
    Ò  &#210;  &Ograve;
    Ó  &#211;  &Oacute;
    Ô  &#212;  &Ocirc;
    Õ  &#213;  &Otilde;
    Ö  &#214;  &Ouml;
    ×  &#215;  &times;
    Ø  &#216;  &Oslash;
    Ù  &#217;  &Ugrave;
    Ú  &#218;  &Uacute;
    Û  &#219;  &Ucirc;
    Ü  &#220;  &Uuml;
    Ý  &#221;  &Yacute;
    Þ  &#222;  &THORN;
    ß  &#223;  &szlig;
    à  &#224;  &agrave;
    á  &#225;  &aacute;
    â  &#226;  &acirc;
    ã  &#227;  &atilde;
    ä  &#228;  &auml;
    å  &#229;  &aring;
    æ  &#230;  &aelig;
    ç  &#231;  &ccedil;
    è  &#232;  &egrave;
    é  &#233;  &eacute;
    ê  &#234;  &ecirc;
    ë  &#235;  &euml;
    ì  &#236;  &igrave;
    í  &#237;  &iacute;
    î  &#238;  &icirc;
    ï  &#239;  &iuml;
    ð  &#240;  &eth;
    ñ  &#241;  &ntilde;
    ò  &#242;  &ograve;
    ó  &#243;  &oacute;
    ô  &#244;  &ocirc;
    õ  &#245;  &otilde;
    ö  &#246;  &ouml;
    ÷  &#247;  &divide;
    ø  &#248;  &oslash;
    ù  &#249;  &ugrave;
    ú  &#250;  &uacute;
    û  &#251;  &ucirc;
    ü  &#252;  &uuml;
    ý  &#253;  &yacute;
    þ  &#254;  &thorn;
    ÿ  &#255;
    Ā  &#256;
    ā  &#257;
    Ă  &#258;
    ă  &#259;
    Ą  &#260;
    ą  &#261;
    Ć  &#262;
    ć  &#263;
    Ĉ  &#264;
    ĉ  &#265;
    Ċ  &#266;
    ċ  &#267;
    Č  &#268;
    č  &#269;
    Ď  &#270;
    ď  &#271;
    Đ  &#272;
    đ  &#273;
    Ē  &#274;
    ē  &#275;
    Ĕ  &#276;
    ĕ  &#277;
    Ė  &#278;
    ė  &#279;
    Ę  &#280;
    ę  &#281;
    Ě  &#282;
    ě  &#283;
    Ĝ  &#284;
    ĝ  &#285;
    Ğ  &#286;
    ğ  &#287;
    Ġ  &#288;
    ġ  &#289;
    Ģ  &#290;
    ģ  &#291;
    Ĥ  &#292;
    ĥ  &#293;
    Ħ  &#294;
    ħ  &#295;
    Ĩ  &#296;
    ĩ  &#297;
    Ī  &#298;
    ī  &#299;
    Ĭ  &#300;
    ĭ  &#301;
    Į  &#302;
    į  &#303;
    İ  &#304;
    ı  &#305;
    Ĳ  &#306;
    ĳ  &#307;
    Ĵ  &#308;
    ĵ  &#309;
    Ķ  &#310;
    ķ  &#311;
    ĸ  &#312;
    Ĺ  &#313;
    ĺ  &#314;
    Ļ  &#315;
    ļ  &#316;
    Ľ  &#317;
    ľ  &#318;
    Ŀ  &#319;
    ŀ  &#320;
    Ł  &#321;
    ł  &#322;
    Ń  &#323;
    ń  &#324;
    Ņ  &#325;
    ņ  &#326;
    Ň  &#327;
    ň  &#328;
    ŉ  &#329;
    Ŋ  &#330;
    ŋ  &#331;
    Ō  &#332;
    ō  &#333;
    Ŏ  &#334;
    ŏ  &#335;
    Ő  &#336;
    ő  &#337;
    Œ  &#338;
    œ  &#339;
    Ŕ  &#340;
    ŕ  &#341;
    Ŗ  &#342;
    ŗ  &#343;
    Ř  &#344;
    ř  &#345;
    Ś  &#346;
    ś  &#347;
    Ŝ  &#348;
    ŝ  &#349;
    Ş  &#350;
    ş  &#351;
    Š  &#352;
    š  &#353;
    Ţ  &#354;
    ţ  &#355;
    Ť  &#356;
    ť  &#357;
    Ŧ  &#358;
    ŧ  &#359;
    Ũ  &#360;
    ũ  &#361;
    Ū  &#362;
    ū  &#363;
    Ŭ  &#364;
    ŭ  &#365;
    Ů  &#366;
    ů  &#367;
    Ű  &#368;
    ű  &#369;
    Ų  &#370;
    ų  &#371;
    Ŵ  &#372;
    ŵ  &#373;
    Ŷ  &#374;
    ŷ  &#375;
    Ÿ  &#376;
    Ź  &#377;
    ź  &#378;
    Ż  &#379;
    ż  &#380;
    Ž  &#381;
    ž  &#382;
    ſ  &#383;
    Ŕ  &#340;
    ŕ  &#341;
    Ŗ  &#342;
    ŗ  &#343;
    Ř  &#344;
    ř  &#345;
    Ś  &#346;
    ś  &#347;
    Ŝ  &#348;
    ŝ  &#349;
    Ş  &#350;
    ş  &#351;
    Š  &#352;
    š  &#353;
    Ţ  &#354;
    ţ  &#355;
    Ť  &#356;
    Ŧ  &#358;
    ŧ  &#359;
    Ũ  &#360;
    ũ  &#361;
    Ū  &#362;
    ū  &#363;
    Ŭ  &#364;
    ŭ  &#365;
    Ů  &#366;
    ů  &#367;
    Ű	&#368;
    ű  &#369;
    Ų	&#370;
    ų  &#371;
    Ŵ &#372;
    ŵ	&#373;
    Ŷ	&#374;
    ŷ  &#375;
    Ÿ  &#376;
    Ź  &#377;
    ź  &#378;
    Ż  &#379;
    ż  &#380;
    Ž  &#381;
    ž  &#382;
    ſ  &#383;
""".strip()


if __name__ == '__main__':

    import sys

    if sys.stdin.isatty():
        sys.exit(1)

    x = sys.stdin.read()
    x = htmltotext(x)

    print x

    if 0:
        no_ent = markup.remove_entities(XXX)

        for orig, line in zip(XXX.split('\n'), (x.strip().split() for x in no_ent.split('\n'))):
            if not line:
                print
                print 'SKIPPED:', orig
                continue
            a = line[0]
            if not all(a == b for b in line):
                print
                print 'INPUT: ', orig.strip()
                print 'OUTPUT:', ' '.join(line).strip()

    if 0:
        A = strip_accents(XXX)
        print A

    if 0:
        B = remove_accents(XXX)
        print B
