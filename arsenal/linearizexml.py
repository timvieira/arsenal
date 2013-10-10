#!/usr/bin/python

# Based on a recipe 
# http://code.activestate.com/recipes/577547-flatten-xml-to-xpath-syntax-lines/

"""
Transforms a XML file into a flat text output, with XPath-like syntax, one line
per XML node or attribute. This format is more suitable for working with
standard unix command-line utils (sed, grep, ... etc).
"""


from xml.etree.ElementTree import parse

def linearize(el, path, numbered=True):

    # print text value if not empty
    text = (el.text or '').strip()
    if not text:
        yield path, ''
    else:
        # Several lines?
        lines = text.splitlines()
        if len(lines) > 1:
            for lineno, line in enumerate(lines):
                yield path + "[line %d]" % (lineno + 1), line
        else:
            yield path, text

    # Print attributes
    for name, val in el.items():
        yield path + "/@" + name, val

    # Counter on the sibling element names
    counter = {}
    for child in el:
        tag = child.tag
        if numbered:
            if tag in counter:     # number tag names which have already occurred
                counter[tag] += 1
                tag = "%s[%d]" % (tag, counter[tag])
            else:
                counter[tag] = 1

        # recurse
        for x in linearize(child, path + '/' + tag):
            yield x

def linearize_stream(stream, prefix='', numbered=True):
    tree = parse(stream)
    root = tree.getroot()
    for x in linearize(root, prefix + "//" + root.tag, numbered=numbered):
        yield x

def process(stream, prefix=''):
    for path, content in linearize_stream(stream, prefix):
        print '%s\t%s' % (path, content)


def main():
    import sys
    if len(sys.argv) > 2:
        print 'sorry one file at a time.'
        sys.exit(1)
    if len(sys.argv) == 2:
        with file(sys.argv[1]) as f:
            process(f)
    else:
        process(sys.stdin)

if __name__ == '__main__':
    main()

