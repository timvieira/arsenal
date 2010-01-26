import csv
from collections import namedtuple
from operator import itemgetter

# countrylist.csv take from:
#   http://www.andrewpatton.com/countrylist.html

rename = [
    ('Sort Order',  'order'),
    ('Common Name', 'common_name'),
    ('Formal Name', 'formal_name'),
    ('Type',        'type'),
    ('Sub Type',    'sub_type'),
    ('Sovereignty', 'sovereignty'),
    ('Capital',     'capital'),
    # country codes
    ('ISO 4217 Currency Code',   'currency_code'),
    ('ISO 4217 Currency Name',   'currency_name'),
    ('ITU-T Telephone Code',     'telephone_code'),
    ('ISO 3166-1 2 Letter Code', 'iso_two_letter_code'),
    ('ISO 3166-1 3 Letter Code', 'iso_three_letter_code'),
    ('ISO 3166-1 Number',        'iso_numeric_code'),
    ('IANA Country Code TLD',    'www_country_code'),
]

Country = namedtuple('Country', map(itemgetter(1), rename), verbose=True)

countries = []
with file('countrylist.csv') as f:
    d = iter(csv.reader(f))
    d.next()  # first row is the fieldnames
    for row in d:
        c = Country(*row)
        countries.append(c)

for c in countries:
    print c.common_name
