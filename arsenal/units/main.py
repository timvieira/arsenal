from unitgroup import UnitGroup
import unitdata, option

UNKNOWN_UNIT         = 'UNKNOWN UNIT'
CONFORMABILITY_ERROR = 'CONFORMABILITY ERROR'

options = option.Option('convertall', 20)
#options.loadAll(["DecimalPlaces 8", "SciNotation yes", "FixedDecimals no"])

data = unitdata.UnitData()
data.readData()

def convert(value, from_unit, to_unit):

    fromUnit = UnitGroup(data, options)
    fromUnit.update(from_unit)
    fromUnit.reduceGroup()
    
    toUnit = UnitGroup(data, options)
    toUnit.update(to_unit)
    toUnit.reduceGroup()

    if not fromUnit.reducedList or not toUnit.reducedList:
        return UNKNOWN_UNIT

    if not fromUnit.categoryMatch(toUnit):
        return CONFORMABILITY_ERROR
    else:
        num = float(value)
        return fromUnit.convert(num, toUnit)
