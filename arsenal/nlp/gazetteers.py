from itertools import ifilter, imap
def linebyline(x):
    return set(imap(str.strip, ifilter(lambda x: x and not x.startswith('#'), x.split('\n'))))


conjunctions = """
for
and
nor
but
or
yet
so
after
because
although
if
before
since
though
unless
when
now that
even though
only if
while
as
whereas
whether or not
since
in order that
while
even if
until
so
in case
in case that
"""

prepositions = """
aboard
about
above
absent
across
after
against
along
alongside
amid
amidst
among
amongst
around
as
astride
at
atop
barring
before
behind
below
beneath
beside
besides
between
beyond
but
by
despite
down
during
except
failing
following
for
from
in
inside
into
like
mid
minus
near
next
notwithstanding
of
off
on
onto
opposite
outside
over
past
plus
regarding
round
save
since
than
through
throughout
till
times
to
toward
towards
under
underneath
unlike
until
up
upon
via
with
within
without
according to
ahead of
as to
aside from
because of
close to
due to
far from
in to
inside of
instead of
near to
next to
on to
out of
outside of
owing to
prior to
subsequent to
as far as
as well as
by means of
in accordance with
in addition to
in front of
in place of
in spite of
on account of
on behalf of
on top of
with regard to
in case of
"""

numbers = """
zero
one
two
three
four
five
six
seven
eight
nine
ten
eleven
twelve
dozen
thirteen
fourteen
fifteen
sixteen
seventeen
eighteen
nineteen
twenty
thirty
fourty
fifty
sixty
seventy
eighty
ninety
hundred
thousand
million
billion
trillion
"""

pronouns = """
he
she
it
him
her
his
hers
its
they
them
their
theirs
I
me
mine
we
us
our
ours
you
your
yours
one
one's
ones
anyone
anybody
anything
someone
somebody
something
everyone
everybody
everything
nothing
nobody
any
each
either
neither
all
most
some
several
none
both
few
many
himself
herself
itself
themselves
themself
myself
ourselves
ourself
oneself
this
that
these
those
who
whom
which
whose
whoever
whomever
whatever
whichever
what
"""

honorifics = """
A.
Adj.
Adm.
Adv.
Asst.
B.
Bart.
Bldg.
Brig.
Bros.
C.
Capt.
Cmdr.
Col.
Comdr.
Con.
Cpl.
D.
DR.
Dr.
E.
Ens.
F.
G.
Gen.
Gov.
H.
Hon.
Hosp.
I.
Insp.
J.
K.
L.
Lt.
M.
M.
MM.
MR.
MRS.
MS.
Maj.
Messrs.
Mlle.
Mme.
Mr.
Mrs.
Ms.
Msgr.
N.
O.
Op.
Ord.
P.
Pfc.
Ph.
Prof.
Pvt.
Q.
R.
Rep.
Reps.
Res.
Rev.
Rt.
S.
Sen.
Sens.
Sfc.
Sgt.
Sr.
St.
Supt.
Surg.
T.
U.
V.
W.
X.
Y.
Z.
v.
vs.
"""

scientific_units = """
kg
kilogram
key
hectogram
dekagram
gram
g
decigram
centigram
milligram
mg
microgram
tonne
metric ton
megagram
kilotonne
gigagram
teragram
carat
ct
amu
atomic mass unit
pound
lb
lbm
ounce
oz
lid
ton
kiloton
slug
stone
grain
m
meter
metre
decimeter
cm
centimeter
mm
millimeter
micrometer
micron
nanometer
nm
dekameter
hectometer
km
kilometer
megameter
angstrom
fermi
inch
in
inches
mil
microinch
microinches
foot
ft
feet
yard
yd
mile
mi
nautical mile
nmi
league
chain
fathom
#rod
furlong
hand
cubit
point
pica
caliber
football field
marathon
au
astronomical unit
light year
light minute
light second
parsec
kiloparsec
megaparsec
screw size
AWG
American Wire Gauge
standard gauge
zinc gauge
ring size
shoe size mens
shoe size womens
s
sec
second
ms
millisecond
microsecond
ns
nanosecond
minute
min
hour
hr
bell
watch
watches
day
week
wk
fortnight
month
year
yr
calendar year
decade
century
centuries
millennium
millennia
man hour
man week
man month
man year
K
Kelvin
deg K
degree Kelvin
C
Celsius
deg C
degree Celsius
R
Rankine
deg R
F
Fahrenheit
deg F
degree Fahrenheit
C deg
Celsius degree
F deg
Fahrenheit degree
A
ampere
amp
milliampere
milliamp
mA
microampere
kiloampere
kA
coulomb
amp hour
mAh
milliamp hour
volt
V
millivolt
mV
kilovolt
kV
ohm
milliohm
microhm
kilohm
siemens
farad
millifarad
microfarad
nanofarad
picofarad
weber
Wb
henry
H
millihenry
mH
microhenry
tesla
T
mol
mole
gram mole
kilomole
kmol
pound mole
lbmol
avogadro
cd
candela
lumen
lm
lux
footcandle
metercandle
lambert
millilambert
footlambert
radian
rad
circle
turn
revolution
rev
degree
deg
arc min
arc minute
min arc
minute arc
arc sec
arc second
sec arc
second arc
quadrant
right angle
gradian
sr
steradian
sphere
hemisphere
bit
kilobit
byte
B
kilobyte
kB
megabyte
MB
gigabyte
GB
terabyte
TB
petabyte
PB
kibibyte
KiB
mebibyte
MiB
gibibyte
GiB
tebibyte
TiB
pebibyte
PiB
bps
kbps
unit
pi
pair
hat trick
dozen
doz
bakers dozen
score
gross
great gross
ream
percent
%
mill
APR
proof
ppm
parts per million
ppb
parts per billion
ppt
parts per trillion
karat
carat gold
newton
N
dekanewton
kilonewton
kN
meganewton
millinewton
dyne
kg force
kgf
kilogram force
gram force
pound force
lbf
ton force
ounce force
ozf
barn
are
decare
dekare
hectare
acre
section
township
homestead
circular inch
circular mil
cc
cubic centimeter
liter
l
litre
deciliter
centiliter
milliliter
ml
dekaliter
hectoliter
kiloliter
kl
megaliter
gallon
gal
quart
qt
pint
pt
fluid ounce
fl oz
ounce fluid
imperial gallon
imp gal
imperial quart
imp qt
imperial pint
imp pt
imperial fluid ounce
imp fl oz
cup
tablespoon
tbsp
teaspoon
tsp
barrel
bbl
shot
fifth
wine bottle
magnum
keg
bushel
peck
cord
board foot
board feet
knot
kt
light speed
mph
kph
mach
rpm
rps
gph
gpm
cfs
cfm
lpm
sccm
sccs
slpm
slph
scfh
scfm
Pa
pascal
kPa
kilopascal
MPa
megapascal
atm
atmosphere
bar
mbar
millibar
microbar
decibar
kilobar
mm Hg
millimeter of Hg
torr
in Hg
inch of Hg
m water
m H2O
meter of water
in water
in H2O
inch of water
ft water
ft H2O
feet of water
foot of head
ft hd
psi
pound per sq inch
ksi
density water
density sea water
density Hg
density air
density steel
density aluminum
density zinc
density brass
density copper
density iron
density nickel
density tin
density titanium
density silver
density nylon
density polycarbonate
joule
J
kilojoule
kJ
megajoule
gigajoule
millijoule
mJ
calorie
cal
kilocalorie
kcal
calorie food
Btu
British thermal unit
erg
electronvolt
eV
kWh
kilowatt hour
ton TNT
watt
W
kilowatt
kW
megawatt
MW
gigawatt
GW
milliwatt
horsepower
hp
metric horsepower
hertz
Hz
millihertz
kilohertz
kHz
megahertz
MHz
gigahertz
GHz
becquerel
Bq
curie
millicurie
roentgen
gray
Gy
rad. abs. dose
sievert
millisievert
Sv
rem
millirem
poise
P
centipoise
cP
stokes
St
centistokes
cSt
gravity
gravity constant
gas constant
mpg
m.p.g.
m.p.s.
bps
b.p.s.
kB/
kb/s
"""

numbers          = linebyline(numbers)
pronouns         = linebyline(pronouns)
prepositions     = linebyline(prepositions)
conjunctions     = linebyline(conjunctions)
honorifics       = linebyline(honorifics)
scientific_units = linebyline(scientific_units)

