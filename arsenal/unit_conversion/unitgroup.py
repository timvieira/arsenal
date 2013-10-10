#!/usr/bin/env python

#****************************************************************************
# unitgroup.py, provides a group of units and does conversions
#
# ConvertAll, a units conversion program
# Copyright (C) 2006, Douglas W. Bell
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License, Version 2.  This program is
# distributed in the hope that it will be useful, but WITTHOUT ANY WARRANTY.
#*****************************************************************************

import re
from math import *
from unitatom import UnitAtom


class UnitGroup:
    """Stores, updates and converts a group of units"""
    maxDecPlcs = 12
    operRegEx = re.compile(r'([\*/])')
    def __init__(self, unitData, option):
        self.unitData = unitData
        self.option = option
        self.unitList = []
        self.currentNum = 0
        self.factor = 1.0
        self.reducedList = []
        self.linear = True

    def update(self, text, cursorPos=None):
        """Decode user entered text into units"""
        self.unitList = self.parseGroup(text)
        if cursorPos != None:
            self.updateCurrentUnit(text, cursorPos)
        else:
            self.currentNum = len(self.unitList) - 1

    def updateCurrentUnit(self, text, cursorPos):
        """Set current unit number"""
        self.currentNum = len(UnitGroup.operRegEx.findall(text[:cursorPos]))

    def currentUnit(self):
        """Return current unit if its a full match, o/w None"""
        if self.unitList and self.unitList[self.currentNum].equiv:
            return self.unitList[self.currentNum]
        return None

    def currentPartialUnit(self):
        """Return unit with at least a partial match, o/w None"""
        if not self.unitList:
            return None
        return self.unitData.findPartialMatch(self.unitList[self.currentNum]\
                                              .name)

    def currentSortPos(self):
        """Return unit near current unit for sorting"""
        if not self.unitList:
            return self.unitData[self.unitData.sortedKeys[0]]
        return self.unitData.findSortPos(self.unitList[self.currentNum]\
                                         .name)

    def replaceCurrent(self, unit):
        """Replace the current unit with unit"""
        if self.unitList:
            exp = self.unitList[self.currentNum].exp
            self.unitList[self.currentNum] = unit.copy()
            self.unitList[self.currentNum].exp = exp
        else:
            self.unitList.append(unit.copy())

    def completePartial(self):
        """Replace a partial unit with a full one"""
        if self.unitList and not self.unitList[self.currentNum].equiv:
            text = self.unitList[self.currentNum].name
            unit = self.unitData.findPartialMatch(text)
            if unit:
                self.replaceCurrent(unit)

    def moveToNext(self, upward):
        """Replace unit with adjacent one based on match or sort position"""
        unit = self.currentSortPos()
        name = unit.name.lower().replace(' ', '')
        num = self.unitData.sortedKeys.index(name) + (upward and -1 or 1)
        if 0 <= num < len(self.unitData.sortedKeys):
            self.replaceCurrent(self.unitData[self.unitData.sortedKeys[num]])

    def addOper(self, mult):
        """Add new operator & blank unit after current, * if mult is true"""
        if self.unitList:
            self.completePartial()
            prevExp = self.unitList[self.currentNum].exp
            self.currentNum += 1
            self.unitList.insert(self.currentNum, UnitAtom(''))
            if (not mult and prevExp > 0) or (mult and prevExp < 0):
                self.unitList[self.currentNum].exp = -1

    def changeExp(self, newExp):
        """Change the current unit's exponent"""
        if self.unitList:
            self.completePartial()
            if self.unitList[self.currentNum].exp > 0:
                self.unitList[self.currentNum].exp = newExp
            else:
                self.unitList[self.currentNum].exp = -newExp

    def clearUnit(self):
        """Remove units"""
        self.unitList = []
        self.currentNum = 0
        self.factor = 1.0
        self.reducedList = []
        self.linear = True

    def parseGroup(self, text):
        """Return list of units from text string"""
        unitList = []
        parts = [part.strip() for part in UnitGroup.operRegEx.split(text)]
        numerator = True
        while parts:
            unit = self.parseUnit(parts.pop(0))
            if not numerator:
                unit.exp = -unit.exp
            if parts and parts.pop(0) == '/':
                numerator = not numerator
            unitList.append(unit)
        return unitList

    def parseUnit(self, text):
        """Return a valid or invalid unit with exponent from a text string"""
        parts = text.split('^', 1)
        exp = 1
        if len(parts) > 1:   # has exponent
            try:
                exp = int(parts[1])
            except ValueError:
                if parts[1].lstrip().startswith('-'):
                    exp = -UnitAtom.partialExp  # tmp invalid exp
                else:
                    exp = UnitAtom.partialExp
        unitText = parts[0].strip().lower().replace(' ', '')
        unit = self.unitData.get(unitText, None)
        if not unit and unitText and unitText[-1] == 's' and not \
           self.unitData.findPartialMatch(unitText):   # check for plural
            unit = self.unitData.get(unitText[:-1], None)
        if not unit:
            unit = UnitAtom(parts[0].strip())   # tmp invalid unit
        unit = unit.copy()
        unit.exp = exp
        return unit

    def unitString(self, unitList=None):
        """Return the full string for this group or a given group"""
        if unitList == None:
            unitList = self.unitList
        fullText = ''
        if unitList:
            fullText = unitList[0].unitText(0)
            numerator = True
            for unit in unitList[1:]:
                if (numerator and unit.exp > 0) \
                   or (not numerator and unit.exp < 0):
                    fullText = '%s * %s' % (fullText, unit.unitText(1))
                else:
                    fullText = '%s / %s' % (fullText, unit.unitText(1))
                    numerator = not numerator
        return fullText

    def groupValid(self):
        """Return True if all unitself.reducedLists are valid"""
        if not self.unitList:
            return False
        for unit in self.unitList:
            if not unit.unitValid():
                return False
        return True

    def reduceGroup(self):
        """Update reduced list of units and factor"""
        self.linear = True
        self.reducedList = []
        self.factor = 1.0
        if not self.groupValid():
            return
        count = 0
        tmpList = self.unitList[:]
        while tmpList:
            count += 1
            if count > 5000:
                raise UnitDataError, 'Circular unit definition'
            unit = tmpList.pop(0)
            if unit.equiv == '!':
                self.reducedList.append(unit.copy())
            elif not unit.equiv:
                raise UnitDataError, 'Invalid conversion for "%s"' % unit.name
            else:
                if unit.fromEqn:
                    self.linear = False
                newList = self.parseGroup(unit.equiv)
                for newUnit in newList:
                    newUnit.exp *= unit.exp
                tmpList.extend(newList)
                self.factor *= unit.factor**unit.exp
        self.reducedList.sort()
        tmpList = self.reducedList[:]
        self.reducedList = []
        for unit in tmpList:
            if self.reducedList and unit == self.reducedList[-1]:
                self.reducedList[-1].exp += unit.exp
            else:
                self.reducedList.append(unit)
        self.reducedList = [unit for unit in self.reducedList if \
                            unit.name != 'unit' and unit.exp != 0]

    def categoryMatch(self, otherGroup):
        """Return True if unit types are equivalent"""
        if not self.checkLinear() or not otherGroup.checkLinear():
            return False
        return self.reducedList == otherGroup.reducedList and \
               [unit.exp for unit in self.reducedList] \
               == [unit.exp for unit in otherGroup.reducedList]

    def checkLinear(self):
        """Return True if linear or acceptable non-linear"""
        if not self.linear:
            if len(self.unitList) > 1 or self.unitList[0].exp != 1:
                return False
        return True

    def compatStr(self):
        """Return string with reduced unit or linear compatability problem"""
        if self.checkLinear():
            return self.unitString(self.reducedList)
        return 'Cannot combine non-linear units'

    def convert(self, num, toGroup):
        """Return num of this group converted to toGroup"""
        if self.linear:
            num *= self.factor
        else:
            num = self.nonLinearCalc(num, 1) * self.factor
        if toGroup.linear:
            return num / toGroup.factor
        return toGroup.nonLinearCalc(num / toGroup.factor, 0)

    def nonLinearCalc(self, num, isFrom):
        """Return result of non-linear calculation"""
        x = num
        try:
            if self.unitList[0].toEqn:      # regular equations
                if isFrom:
                    return float(eval(self.unitList[0].fromEqn))
                return float(eval(self.unitList[0].toEqn))
            data = list(eval(self.unitList[0].fromEqn))  # extrapolation list
            if isFrom:
                data = [(float(group[0]), float(group[1])) for group in data]
            else:
                data = [(float(group[1]), float(group[0])) for group in data]
            data.sort()
            pos = len(data) - 1
            for i in range(len(data)):
                if num <= data[i][0]:
                    pos = i
                    break
            if pos == 0:
                pos = 1
            return (num-data[pos-1][0]) / float(data[pos][0]-data[pos-1][0]) \
                   * (data[pos][1]-data[pos-1][1]) + data[pos-1][1]
        except OverflowError:
            return 1e9999
        except:
            raise UnitDataError, 'Bad equation for %s' % self.unitList[0].name

    def convertStr(self, num, toGroup):
        """Return formatted string of converted number"""
        return self.formatNumStr(self.convert(num, toGroup))

    def formatNumStr(self, num):
        """Return num string formatted per options"""
        decPlcs = self.option.intData('DecimalPlaces', 0, UnitGroup.maxDecPlcs)
        if self.option.boolData('SciNotation'):
            return ('%%0.%dE' % decPlcs) % num
        if self.option.boolData('FixedDecimals'):
            return ('%%0.%df' % decPlcs) % num
        return ('%%0.%dG' % decPlcs) % num




