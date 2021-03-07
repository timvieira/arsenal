from arsenal.nlp.annotation import bio2span, Span

def test_bio2span():

    tests = [
        (['I-NUM','I-TEMP'], [Span(label='NUM', begins=0, ends=1), Span(label='TEMP', begins=1, ends=2)]),
        (['I-NUM','B-TEMP'], [Span(label='NUM', begins=0, ends=1), Span(label='TEMP', begins=1, ends=2)]),
        (['B-NUM','B-TEMP'], [Span(label='NUM', begins=0, ends=1), Span(label='TEMP', begins=1, ends=2)]),
        (['B-NUM','B-TEMP'], [Span(label='NUM', begins=0, ends=1), Span(label='TEMP', begins=1, ends=2)]),
        (['B-NUM','O'], [Span(label='NUM', begins=0, ends=1)]),
        (['O','B-NUM'], [Span(label='NUM', begins=1, ends=2)]),
        (['O','B-NUM','O'], [Span(label='NUM', begins=1, ends=2)]),
        (['O','B-NUM','I-NUM'], [Span(label='NUM', begins=1, ends=3)]),
        (
            ['O', 'O', 'O',
             'I-NUM', 'I-NUM', 'I-NUM',
             'I-TEMP', 'I-TEMP', 'I-TEMP', 'I-TEMP', 'I-TEMP', 'I-TEMP', 'I-TEMP', 'I-TEMP',
             'O',
             'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM',
             'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            [Span(label='NUM', begins=3, ends=6),
             Span(label='TEMP', begins=6, ends=14),
             Span(label='NUM', begins=15, ends=23)
             ]
        ),
        (
            ['O', 'O', 'O', 'O', 'O', 'O',
             'I-TEMP',
             'I-NUM', 'I-NUM', 'I-NUM',
             'O',
             'I-NUM', 'I-NUM', 'I-NUM', 'I-NUM',
             'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
             'I-TEMP', 'I-TEMP', 'I-TEMP',
             'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            [Span(label='TEMP', begins=6, ends=7),
             Span(label='NUM', begins=7, ends=10),
             Span(label='NUM', begins=11, ends=15),
             Span(label='TEMP', begins=23, ends=26),
             ]
        ),
        (
            ['O', 'O', 'O',
             'B-NUM', 'I-NUM', 'I-NUM', 'I-NUM' ,
             'B-NUM', 'I-NUM', 'I-NUM', 'I-NUM',
             'O',
             'B-NUM', 'I-NUM', 'I-NUM',
             'O', 'O', 'O',
             'B-TEMP', 'I-TEMP',
             'O'],
            [Span(label='NUM', begins=3, ends=7),
             Span(label='NUM', begins=7, ends=11),
             Span(label='NUM', begins=12, ends=15),
             Span(label='TEMP', begins=18, ends=20),
             ]
        ),
    ]

    for x, want in tests:
        print(x)
        have = bio2span(x, include_O=False)
        if want == have:
            print('\033[32mpassed\033[0m')
        else:
            print('\033[31mfailed:\033[0m')
            print('  want:', want)
            print('       have:', have)
        print()


    print('*************************************************************************')
    print('** Including O Spans.')

    include_O = [
        (['O','B-NUM','I-DATE'],
         [Span(label='O', begins=0, ends=1),
          Span(label='NUM', begins=1, ends=2),
          Span(label='DATE', begins=2, ends=3)]
        ),
        (['O','B-NUM','O','I-DATE'],
         [Span(label='O', begins=0, ends=1), Span(label='NUM', begins=1, ends=2), Span(label='O', begins=2, ends=3),
          Span(label='DATE', begins=3, ends=4)]
        ),
        (['O','B-NUM','O','I-DATE', 'O', 'O'],
         [Span(label='O', begins=0, ends=1),
          Span(label='NUM', begins=1, ends=2),
          Span(label='O', begins=2, ends=3),
          Span(label='DATE', begins=3, ends=4),
          Span(label='O', begins=4, ends=5),
          Span(label='O', begins=5, ends=6)]
         ),
        (['O'],
         [Span(label='O', begins=0, ends=1)]
        ),
    ]

    for x, want in include_O:
        print(x)
        have = bio2span(x, include_O=True)
        if want == have:
            print('\033[32mpassed\033[0m')
        else:
            print('\033[31mfailed:\033[0m')
            print('  want:', want)
            print('  have:', have)
            raise AssertionError
        print()

    print('passed test_bio2span')


if __name__ == '__main__':
    test_bio2span()
