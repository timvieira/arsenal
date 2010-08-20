import re

def xml2segments(x):
    """
    Generate BIO-token pairs from xml-style annotation.
    Notes:
      1) Splits text on spaces, so wordsplitting should already be done.
      2) Assumes no self-closing tags
      3) Assumes no nesting (tags within tags)
      4) Converts newlines into a token "-NEWLINE-"

    >>> x = xml2segments("<title>Cat in the Hat</title><author>Dr. Seuss</author>")
    >>> list(x)
    [('title', ['Cat', 'in', 'the', 'Hat']), ('author', ['Dr.', 'Seuss'])]

    """
    x = re.sub('\n', ' -NEWLINE- ', x)
    x = re.sub('(<[/]?[A-Za-z0-9]+>)', r' \1 ', x)
    for label, tagged, close, word in re.findall('(?:(?:\s*<([A-Za-z0-9]+)>\s*([\w\W]+?)\s*</([A-Za-z0-9]+)>\s*)|([\w\W]+?)(?:\s+|$))', x):
        assert close == label, (close, label)
        if word:
            yield ('O', [word])
        else:
            yield (label, tagged.split())

