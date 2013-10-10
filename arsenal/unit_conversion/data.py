data = """
#*****************************************************************************
# ConvertAll, a units conversion program
# Copyright (C) 2005, Douglas W. Bell
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License, Version 2.  This program is
# distributed in the hope that it will be useful, but WITTHOUT ANY WARRANTY.
#*****************************************************************************
#
# Units are defined by an optional quantity and an equivalent unit or unit
# combination.  A python expression may be used for the quantity, but is
# resticted to using only the following operators: *, /, +, -, **, (, ).
# Beware of integer division truncation: be sure to use a float for at
# least one of the values.
#
# The unit type must be placed in square brackets before a set of units.
# The first comment after the equivalent unit will be put in parenthesis after
# the unit name (usually used to give the full name of an abbreviated unit).
# The next comment will be used in the program list's comment column;
# later comments and full line comments are ignored.
#
# Non-linear units are indicated with an equivalent unit in square brackets,
# followed by either equations or equivalency lists for the definition.
# For equations, two are given, separated by a ';'.  Both are functions of
# "x", the first going from the unit to the equivalent unit and the second
# one in reverse.  Any valid Python expression returning a float (including 
# the functions in the math module) should work.  The equivalency list is a 
# python list of tuples giving points for linear interpolation.
#
# All units must reduce to primitive units, which are indicated by an '!'
# as the equivalent unit.  Circular refernces must also be avoided.
#
# Primitive units:  kg, m, s, K, A, mol, cd, rad, sr, bit, unit
#
##############################################################################

#
# mass units
#
[mass]
kg                = !                  # kilogram
kilogram          = kg
key               = kg                 # # drug slang
hectogram         = 100 gram
dekagram          = 10 gram
gram              = 0.001 kg
g                 = gram               # gram
decigram          = 0.1 gram
centigram         = 0.01 gram
milligram         = 0.001 gram
mg                = milligram          # milligram
microgram         = 0.001 mg
tonne             = 1000 kg            # # metric
metric ton        = tonne
megagram          = tonne
kilotonne         = 1000 tonne         # # metric
gigagram          = 1e9 gram
teragram          = 1e12 gram
carat             = 0.2 gram
ct                = carat              # carat
amu               = 1.66053873e-27 kg  # atomic mass
atomic mass unit  = amu
pound             = 0.45359237 kg
lb                = pound              # pound
lbm               = pound              # pound
ounce             = 1/16.0 pound
oz                = ounce              # ounce
lid               = ounce              # # drug slang
ton               = 2000 lb            # # non-metric
kiloton           = 1000 ton           # # non-metric
slug              = lbf*s^2/ft
stone             = 14 lb
grain             = 1/7000.0 lb


#
# length / distance units
#
[length]
m                    = !              # meter
meter                = m
metre                = m
decimeter            = 0.1 m
cm                   = 0.01 m         # centimeter
centimeter           = cm
mm                   = 0.001 m        # millimeter
millimeter           = mm
micrometer           = 1e-6 m
micron               = micrometer
nanometer            = 1e-9 m
nm                   = nanometer      # nanometer
dekameter            = 10 m
hectometer           = 100 m
km                   = 1000 m         # kilometer
kilometer            = km
megameter            = 1000 km
angstrom             = 1e-10 m
fermi                = 1e-15 m        # # nuclear sizes
inch                 = 2.54 cm
in                   = inch           # inch
inches               = inch
mil                  = 0.001 inch
microinch            = 1e-6 inch
microinches          = microinch
foot                 = 12 inch
ft                   = foot           # foot
feet                 = foot
yard                 = 3 ft
yd                   = yard           # yard
mile                 = 5280 ft
mi                   = mile           # mile
nautical mile        = 1852 m
nmi                  = nautical mile  # nautical mile
league               = 3 mile
chain                = 66 ft
fathom               = 6 ft
rod                  = 5.5 yard
furlong              = 40 rod
hand                 = 4 inch
cubit                = 21.8 inch      # # biblical unit
point                = 1/72.27 inch
pica                 = 12 point
caliber              = 0.01 inch      # # bullet sizes
football field       = 100 yd
marathon             = 46145 yd
au                   = 1.49597870691e11 m   # astronomical unit
astronomical unit    = au
light year           = 365.25 light speed * day
light minute         = light speed * min
light second         = light speed * s
parsec               = 3.0856775813e16 m
kiloparsec           = 1000 parsec
megaparsec           = 1000 kiloparsec
screw size           = [in] 0.013*x + 0.06 ; (x - 0.06) / 0.013 \
                       # # Unified diameters, non-linear
AWG                  = [in] 92.0**((36-x)/39.0)/200.0 ; \
                       36 - 39.0*log(200.0*x)/log(92.0) \
                       # American Wire Gauge \
                       # use -1, -2 for 00, 000; non-linear
American Wire Gauge  = [in] 92.0**((36-x)/39.0)/200.0 ; \
                       36 - 39.0*log(200.0*x)/log(92.0) \
                       #  # use -1, -2 for 00, 000; non-linear
standard gauge       = [in] [(-5, .448350), (1, .269010), (14, .0747250), \
                       (16, .0597800), (17, .0538020), (20, .0358680), \
                       (26, .0179340), (31, .0104615), (36, .00672525), \
                       (38, .00597800)] # steel \
                       # Manufacturers Std. Gauge, non-linear
zinc gauge           = [in] [(1, .002), (10, .02), (15, .04), (19, .06), \
                       (23, .1), (24, .125), (27, .5), (28, 1)]  \
                       # # sheet metal thickness, non-linear
ring size            = [in] 0.1018*x + 1.4216 ; (x - 1.4216) / 0.1018  \
                       # # US size, circum., non-linear
shoe size mens       = [in] x/3.0 + 7 + 1/3.0 ; (x - 7 - 1/3.0) * 3 \
                       # # US sizes, non-linear
shoe size womens     = [in] x/3.0 + 6 + 5/6.0 ; (x - 6 - 5/6.0) * 3 \
                       # # US sizes, non-linear


#
# time units
#
[time]
s             = !                 # second
sec           = s                 # second
second        = s
ms            = 0.001 s           # millisecond
millisecond   = ms
microsecond   = 1e-6 s
ns            = 1e-9 s            # nanosecond
nanosecond    = ns
minute        = 60 s
min           = minute            # minute
hour          = 60 min
hr            = hour              # hour
bell          = 30 min            #  # naval definition
watch         = 4 hour
watches       = watch
day           = 24 hr
week          = 7 day
wk            = week              # week
fortnight     = 14 day
month         = 1/12.0 year
year          = 365.242198781 day
yr            = year              # year
calendar year = 365 day
decade        = 10 year
century       = 100 year
centuries     = century
millennium    = 1000 year
millennia     = millennium
[scheduling]
man hour      = 168/40.0 hour
man week      = 40 man hour
man month     = 1/12.0 man year
man year      = 52 man week


#
# temperature
#
[temperature]
K                 = !     # Kelvin
Kelvin            = K
deg K             = K     # Kelvin
degree Kelvin     = K

C                 = [K] x + 273.15 ; x - 273.15  # Celsius  # non-linear
Celsius           = [K] x + 273.15 ; x - 273.15  #          # non-linear
deg C             = [K] x + 273.15 ; x - 273.15  # Celsius  # non-linear
degree Celsius    = [K] x + 273.15 ; x - 273.15  #          # non-linear

R                 = 5/9.0 K     # Rankine
Rankine           = R
deg R             = R           # Rankine
F                 = [R] x + 459.67 ; x - 459.67  # Fahrenheit  # non-linear
Fahrenheit        = [R] x + 459.67 ; x - 459.67  #             # non-linear
deg F             = [R] x + 459.67 ; x - 459.67  # Fahrenheit  # non-linear
degree Fahrenheit = [R] x + 459.67 ; x - 459.67  #             # non-linear

[temp. diff.]
C deg             = K        # Celsius degree
Celsius degree    = C deg
F deg             = R        # Fahrenheit deg.
Fahrenheit degree = F deg


#
# electrical units
#
[current]
A              = !              # ampere
ampere         = A
amp            = A
milliampere    = 0.001 A
milliamp       = milliampere
mA             = milliampere    # milliampere
microampere    = 0.001 mA
kiloampere     = 1000 A
kA             = kiloampere     # kiloampere
[charge]
coulomb        = A*s
amp hour       = A*hr
mAh            = 0.001 amp hour # milliamp hour
milliamp hour  = mAh
[potential]
volt           = W/A
V              = volt           # volt
millivolt      = 0.001 volt
mV             = millivolt      # millivolt
kilovolt       = 1000 volt
kV             = kilovolt       # kilovolt
[resistance]
ohm            = V/A
milliohm       = 0.001 ohm
microhm        = 0.001 milliohm
kilohm         = 1000 ohm
[conductance]
siemens        = A/V
[capacitance]
farad          = coulomb/V
millifarad     = 0.001 farad
microfarad     = 0.001 millifarad
nanofarad      = 1e-9 farad
picofarad      = 1e-12 farad
[magn. flux]
weber          = V*s
Wb             = weber          # weber
[inductance]
henry          = Wb/A
H              = henry          # henry
millihenry     = 0.001 henry
mH             = millihenry     # millihenry
microhenry     = 0.001 mH
[flux density]
tesla          = Wb/m^2
T              = tesla          # tesla


#
# molecular units
#
[molecular qty]
mol          = !           # mole       # gram mole
mole         = mol         #            # gram mole
gram mole    = mol
kilomole     = 1000 mol
kmol         = kilomole    # kilomole
pound mole   = mol*lbm/gram
lbmol        = pound mole  # pound mole
[size of a mol]
avogadro     = gram/amu*mol


#
# Illumination units
#
[lum. intens.]
cd          = !          # candela
candela     = cd

[luminous flux]
lumen        = cd * sr
lm           = lumen     # lumen

[illuminance]
lux          = lumen/m^2
footcandle   = lumen/ft^2
metercandle  = lumen/m^2

[luminance]
lambert      = cd/pi*cm^2
millilambert = 0.001 lambert
footlambert  = cd/pi*ft^2


#
# angular units
#
[angle]
radian      = !
rad         = radian         # radian
circle      = 2 pi*radian
turn        = circle
revolution  = circle
rev         = revolution     # revolution
degree      = 1/360.0 circle
deg         = degree         # degree
arc min     = 1/60.0 degree  # minute
arc minute  = arc min
min arc     = arc min        # minute
minute arc  = arc min
arc sec     = 1/60.0 arc min # second
arc second  = arc sec
sec arc     = arc sec        # second
second arc  = arc sec
quadrant    = 1/4.0 circle
right angle = quadrant
gradian     = 0.01 quadrant


#
# solid angle units
#
[solid angle]
sr         = !      # steradian
steradian  = sr
sphere     = 4 pi*sr
hemisphere = 1/2.0 sphere


#
# information units
#
[data]
bit       = !
kilobit   = 1000 bit   #           # based on power of 10
byte      = 8 bit
B         = byte       # byte
kilobyte  = 1024 byte  #           # based on power of 2
kB        = kilobyte   # kilobyte  # based on power of 2
megabyte  = 1024 kB    #           # based on power of 2
MB        = megabyte   # megabyte  # based on power of 2
gigabyte  = 1024 MB    #           # based on power of 2
GB        = gigabyte   # gigabyte  # based on power of 2
terabyte  = 1024 GB    #           # based on power of 2
TB        = terabyte   # terabyte  # based on power of 2
petabyte  = 1024 TB    #           # based on power of 2
PB        = petabyte   # petabyte  # based on power of 2

kibibyte  = 1024 byte
KiB       = kibibyte   # kibibyte
mebibyte  = 1024 KiB
MiB       = mebibyte   # mebibyte
gibibyte  = 1024 MiB
GiB       = gibibyte   # gibibyte
tebibyte  = 1024 GiB
TiB       = tebibyte   # tebibyte
pebibyte  = 1024 TiB
PiB       = pebibyte   # pebibyte

[data transfer]
bps       = bit/sec    # bits / second
kbps      = 1000 bps   # kilobits / sec.  # based on power of 10


#
# Unitless numbers
#
[quantity]
unit               = !
1                  = unit            # unit
pi                 = 3.14159265358979323846 unit
pair               = 2 unit
hat trick          = 3 unit          # # sports
dozen              = 12 unit
doz                = dozen           # dozen
bakers dozen       = 13 unit
score              = 20 unit
gross              = 144 unit
great gross        = 12 gross
ream               = 500 unit
percent            = 0.01 unit
%                  = percent
mill               = 0.001 unit
[interest rate]
APR                = [unit] log(1 + x/100) ;  (exp(x) - 1)*100 \
                     # annual % rate # based on continuous compounding
[concentration]
proof              = 1/200.0 unit    # # alcohol content
ppm                = 1e-6 unit       # parts per million
parts per million  = ppm
ppb                = 1e-9 unit       # parts per billion
parts per billion  = ppb
ppt                = 1e-12 unit      # parts per trillion
parts per trillion = ppt
karat              = 1/24.0 unit     # # gold purity
carat gold         = karat           # # gold purity


#
# force units
#
[force]
newton         = kg*m/s^2
N              = newton          # newton
dekanewton     = 10 newton
kilonewton     = 1000 N
kN             = kilonewton      # kilonewton
meganewton     = 1000 kN
millinewton    = 0.001 N
dyne           = cm*g/s^2
kg force       = kg * gravity    # kilogram f
kgf            = kg force        # kilogram force
kilogram force = kg force
gram force     = g * gravity
pound force    = lbm * gravity
lbf            = pound force     # pound force
ton force      = ton * gravity
ounce force    = ounce * gravity
ozf            = ounce force     # ounce force


#
# area units
#
[area]
barn          = 1e-28 m^2       # # particle physics
are           = 100 m^2
decare        = 10 are
dekare        = 10 are
hectare       = 100 are
acre          = 10 chain^2
section       = mile^2
township      = 36 section
homestead     = 160 acre
circular inch = 1/4.0 pi*in^2   # # area of 1 inch circle
circular mil  = 1/4.0 pi*mil^2  # # area of 1 mil circle


#
# volume units
#
[volume]
cc                   = cm^3                 # cubic centimeter
cubic centimeter     = cc
liter                = 1000 cc
l                    = liter                # liter
litre                = liter
deciliter            = 0.1 liter
centiliter           = 0.01 liter
milliliter           = cc
ml                   = milliliter           # milliliter
dekaliter            = 10 liter
hectoliter           = 100 liter
kiloliter            = 1000 liter
kl                   = kiloliter            # kiloliter
megaliter            = 1000 kiloliter
gallon               = 231 in^3             #             # US liquid
gal                  = gallon               # gallon      # US liquid
quart                = 1/4.0 gallon         #             # US liquid
qt                   = quart                # quart       # US liquid
pint                 = 1/2.0 quart          #             # US liquid
pt                   = pint                 # pint        # US liquid
fluid ounce          = 1/16.0 pint          #             # US
fl oz                = fluid ounce          # fluid ounce # US
ounce fluid          = fluid ounce          #             # US
imperial gallon      = 4.54609 liter
imp gal              = imperial gallon      # imperial gallon
imperial quart       = 1/4.0 imp gal
imp qt               = imperial quart       # imperial quart
imperial pint        = 1/8.0 imp gal
imp pt               = imperial pint        # imperial pint
imperial fluid ounce = 1/160.0 imp gal
imp fl oz            = imperial fluid ounce # imperial fluid ounce
cup                  = 8 fl oz
tablespoon           = 1/16.0 cup
tbsp                 = tablespoon           # tablespoon
teaspoon             = 1/3.0 tbsp
tsp                  = teaspoon             # teaspoon
barrel               = 42 gallon
bbl                  = barrel               # barrel
shot                 = 1.5 fl oz
fifth                = 1/5.0 gallon         #             # alcohol
wine bottle          = 750 ml
magnum               = 1.5 liter            #             # alcohol
keg                  = 15.5 gallon          #             # beer
bushel               = 2150.42 in^3
peck                 = 1/4.0 bushel
cord                 = 128 ft^3
board foot           = ft^2*in
board feet           = board foot


#
# velocity units
#
[velocity]
knot        = nmi/hr
kt          = knot             # knot
light speed = 2.99792458e8 m/s
mph         = mi/hr            # miles/hour
kph         = km/hr            # kilometers/hour
mach        = 331.46 m/s       # # speed sound at STP
[rot. velocity]
rpm         = rev/min          # rev/min
rps         = rev/sec          # rev/sec


#
# flow rate units
#
[fluid flow]
gph         = gal/hr           # gallons/hour
gpm         = gal/min          # gallons/minute
cfs         = ft^3/sec         # cu ft/second
cfm         = ft^3/min         # cu ft/minute
lpm         = l/min            # liter/min
[gas flow]
sccm        = atm*cc/min       # std cc/min      # pressure * flow
sccs        = atm*cc/sec       # std cc/sec      # pressure * flow
slpm        = atm*l/min        # std liter/min   # pressure * flow
slph        = atm*l/hr         # std liter/hour  # pressure * flow
scfh        = atm*ft^3/hour    # std cu ft/hour  # pressure * flow
scfm        = atm*ft^3/min     # std cu ft/min   # pressure * flow


#
# pressure units
#
[pressure]
Pa                    = N/m^2                    # pascal
pascal                = Pa
kPa                   = 1000 Pa                  # kilopascal
kilopascal            = kPa
MPa                   = 1000 kPa                 # megapascal
megapascal            = MPa
atm                   = 101325 Pa                # atmosphere
atmosphere            = atm
bar                   = 1e5 Pa
mbar                  = 0.001 bar                # millibar
millibar              = mbar
microbar              = 0.001 mbar
decibar               = 0.1 bar
kilobar               = 1000 bar
mm Hg                 = mm*density Hg*gravity
millimeter of Hg      = mm Hg
torr                  = mm Hg
in Hg                 = in*density Hg*gravity    # inch of Hg
inch of Hg            = in Hg
m water               = m*density water*gravity  # meter of H2O
m H2O                 = m water                  # meter of H2O
meter of water        = m water
in water              = in*density water*gravity # inch of H2O
in H2O                = in water                 # inch of H2O
inch of water         = in water
ft water              = ft*density water*gravity # feet of H2O
ft H2O                = ft water                 # feet of H20
feet of water         = ft water
foot of head          = ft water
ft hd                 = ft water                 # foot of head
psi                   = lbf/in^2                 # pound / sq inch
pound per sq inch     = psi
ksi                   = 1000 psi                 # 1000 lb / sq inch


#
# density units
#
[density]
density water         = gram/cm^3
density sea water     = 1.025 gram/cm^3
density Hg            = 13.5950981 gram/cm^3
density air           = 1.293 kg/m^3          # # at STP
density steel         = 0.283 lb/in^3         # # carbon steel
density aluminum      = 0.098 lb/in^3
density zinc          = 0.230 lb/in^3
density brass         = 0.310 lb/in^3         # # 80Cu-20Zn
density copper        = 0.295 lb/in^3
density iron          = 0.260 lb/in^3         # # cast iron
density nickel        = 0.308 lb/in^3
density tin           = 0.275 lb/in^3
density titanium      = 0.170 lb/in^3
density silver        = 0.379 lb/in^3
density nylon         = 0.045 lb/in^3
density polycarbonate = 0.045 lb/in^3


#
# energy units
#
[energy]
joule                = N*m
J                    = joule             # joule
kilojoule            = 1000 joule
kJ                   = kilojoule         # kilojoule
megajoule            = 1000 kilojoule
gigajoule            = 1000 megajoule
millijoule           = 0.001 joule
mJ                   = millijoule        # millijoule
calorie              = 4.1868 J
cal                  = calorie           # calorie
kilocalorie          = 1000 cal
kcal                 = kilocalorie       # kilocalorie
calorie food         = kilocalorie
Btu                  = cal*lb*R/g*K      # British thermal unit
British thermal unit = Btu
erg                  = cm*dyne
electronvolt         = 1.602176462e-19 J
eV                   = electronvolt      # electronvolt
kWh                  = kW*hour           # kilowatt-hour
kilowatt hour        = kWh
ton TNT              = 4.184e9 J


#
# power units
#
[power]
watt              = J/s
W                 = watt            # watt
kilowatt          = 1000 W
kW                = kilowatt        # kilowatt
megawatt          = 1000 kW
MW                = megawatt        # megawatt
gigawatt          = 1000 MW
GW                = gigawatt        # gigawatt
milliwatt         = 0.001 W
horsepower        = 550 ft*lbf/sec
hp                = horsepower      # horsepower
metric horsepower = 75 kgf*m/s


#
# frequency
#
[frequency]
hertz       = unit/sec
Hz          = hertz      # hertz
millihertz  = 0.001 Hz
kilohertz   = 1000 Hz
kHz         = kilohertz  # kilohertz
megahertz   = 1000 kHz
MHz         = megahertz  # megahertz
gigahertz   = 1000 MHz
GHz         = gigahertz  # gigahertz


#
# radioactivity
#
[radioactivity]
becquerel       = unit/sec
Bq              = becquerel     # becquerel
curie           = 3.7e10 Bq
millicurie      = 0.001 curie
roentgen        = 2.58e-4 coulomb/kg
[radiation dose]
gray            = J/kg
Gy              = gray          # gray
rad. abs. dose  = 0.001 Gy      # # commonly rad
sievert         = J/kg          # # equiv. dose
millisievert    = 0.001 sievert # # equiv. dose
Sv              = sievert       # sievert # equiv. dose
rem             = 0.01 Sv       # # roentgen equiv mammal
millirem        = 0.001 rem     # # roentgen equiv mammal


#
# viscosity
#
[dyn viscosity]
poise        = g/cm*s
P            = poise       # poise
centipoise   = 0.01 poise
cP           = centipoise  # centipoise

[kin viscosity]
stokes       = cm^2/s
St           = stokes      # stokes
centistokes  = 0.01 stokes
cSt          = centistokes # centistokes


#
# misc. units
#
[acceleration]
gravity                = 9.80665 m/s^2
[constant]
gravity constant       = 6.673e-11 N*m^2/kg^2
gas constant           = 8.314472 J/mol*K     # R
[fuel consumpt.]
mpg                    = mi/gal               # miles/gallon
"""
