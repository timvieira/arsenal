#!/usr/bin/env python

import sys, os.path
try:
    from __main__ import dataFilePath
except ImportError:
    dataFilePath = None

import unitatom

class UnitDataError(Exception):
    pass

class UnitData(dict):
    def __init__(self):
        dict.__init__(self)
        self.sortedKeys = []
        self.typeList = []

    def findDataFile(self, pathList):
        """Search paths for file, return line list or None"""
        import data
        return data.data.split('\n')

    def readData(self):
        """Read all unit data from file"""
        modPath = os.path.abspath(sys.path[0])
        pathList = [dataFilePath, os.path.join(modPath, '../data/'), modPath]
        lines = self.findDataFile(filter(None, pathList))
        for i in range(len(lines)):     # join continuation lines
            delta = 1
            while lines[i].rstrip().endswith('\\'):
                lines[i] = ''.join([lines[i].rstrip()[:-1], lines[i+delta]])
                lines[i+delta] = ''
                delta += 1
        units = [unitatom.UnitAtom(line) for line in lines if line.split('#', 1)[0].strip()]   # remove comment lines
        typeText = ''
        for unit in units:               # find & set headings
            if unit.name.startswith('['):
                typeText = unit.name[1:-1].strip()
                self.typeList.append(typeText)
            unit.typeName = typeText
        units = [unit for unit in units if unit.equiv]  # keep valid units
        for unit in units:
            self[unit.name.lower().replace(' ', '')] = unit
        self.sortedKeys = self.keys()
        self.sortedKeys.sort()
        if len(self.sortedKeys) < len(units):
            raise UnitDataError, 'Duplicate unit names found'

    def findPartialMatch(self, text):
        """Return first partially matching unit or None"""
        text = text.lower().replace(' ', '')
        if not text:
            return None
        for name in self.sortedKeys:
            if name.startswith(text):
                return self[name]
        return None

    def findSortPos(self, text):
        """Return unit whose abbrev comes immediately after text"""
        text = text.lower().replace(' ', '')
        for name in self.sortedKeys:
            if text <= name:
                return self[name]
        return self[self.sortedKeys[-1]]

    def filteredList(self, type='', srchStr=''):
        """Return list of units matching type and search string,
           if given"""
        units = self.values()
        if type:
            units = [unit for unit in units if unit.typeName == type]
        if srchStr.strip():
            srchWords = [word.lower() for word in srchStr.split()]
            srchUnits = []
            for unit in units:
                if unit.matchWords(srchWords):
                    srchUnits.append(unit)
            units = srchUnits
        return units
