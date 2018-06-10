import re

from arsenal.nlp.annotation import sgml2bio, line_groups, bio2span

def equals_mod_whitespace(a,b):
    """ check if strings are equal ignoring differences in whitespace. """
    return re.sub('\s*', '', a) == re.sub('\s*', '', b)

def test_sgml_reconstruction():
    reference_dataset = '/home/timv/projects/crf/data/tagged_references.txt'

    with open(reference_dataset, 'r') as f:
        for sgml in line_groups(f.read(), '<NEW.*?>'):

            (labels, tokens) = list(zip(*sgml2bio(sgml)))

            # convert spans to sgml
            spans = bio2span(labels)
            reconstructed = ' '.join('<%s>%s</%s>' % (l, ' '.join(tokens[b:e]), l) for (l,b,e) in spans)

            assert equals_mod_whitespace(reconstructed, sgml), \
                'reconstructed example should only differ in whitespace.'

    print('passed sgml reconstruction test.')

if __name__ == '__main__':
    test_sgml_reconstruction()
