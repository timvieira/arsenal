from arsenal.nlp.annotation import sgml2bio, bio2span


def test_sgml_reconstruction():
    sgml = '<author>John Smith</author> <title>A Good Book</title> <date>2024</date>'

    (labels, tokens) = list(zip(*sgml2bio(sgml)))

    spans = bio2span(labels)
    reconstructed = ' '.join(
        '<%s>%s</%s>' % (l, ' '.join(tokens[b:e]), l)
        for (l, b, e) in spans
    )

    assert reconstructed == sgml
