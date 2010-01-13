#!/usr/bin/env python

#****************************************************************************
# option.py, provides classes to read and set user preferences
#
# Copyright (C) 2004, Douglas W. Bell
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License, Version 2.  This program is
# distributed in the hope that it will be useful, but WITTHOUT ANY WARRANTY.
#*****************************************************************************

import sys, os.path, codecs

class Option:
    """Stores and retrieves string options"""
    def __init__(self, fileName, keySpaces=20):
        self.path = ''
        if fileName:
            self.path = os.environ.get('HOME', '')
            if os.path.exists(self.path) and sys.platform != 'win32':
                self.path = os.path.join(self.path, '.' + fileName)
            else:
                self.path = os.path.join(os.path.abspath(sys.path[0]), \
                                         '%s.ini' % fileName)
        self.keySpaces = keySpaces
        self.dfltDict = {}
        self.userDict = {}
        self.dictList = (self.userDict, self.dfltDict)
        self.chgList = []

    def loadAll(self, defaultList):
        """Reads defaultList & file, writes file if required
           return true if file read"""
        self.loadSet(defaultList, self.dfltDict)
        if self.path:
            try:
                f = codecs.open(self.path, 'r', 'utf-8')
            except IOError:
                try:
                    f = codecs.open(self.path, 'w', 'utf-8')
                except IOError:
                    print 'Error - could not write to config file', self.path
                else:
                    f.writelines([line + '\n' for line in defaultList])
                    f.close()
            else:
                self.loadSet(f.readlines(), self.userDict)
                f.close()
                return 1
        return 0

    def loadSet(self, list, data):
        """Reads settings from list into dict"""
        for line in list:
            line = line.split('#', 1)[0].strip()
            if line:
                item = line.split(None, 1) + ['']   # add value if blank
                data[item[0]] = item[1].strip()

    def addData(self, key, strData, storeChange=0):
        """Add new entry, add to write list if storeChange"""
        self.userDict[key] = strData
        if storeChange:
            self.chgList.append(key)

    def boolData(self, key):
        """Returns true or false from yes or no in option data"""
        for data in self.dictList:
            val = data.get(key)
            if val and val[0] in ('y', 'Y'):
                return 1
            if val and val[0] in ('n', 'N'):
                return 0
        print 'Option error - bool key', key, 'is not valid'
        return 0

    def numData(self, key, min=None, max=None):
        """Return float from option data"""
        for data in self.dictList:
            val = data.get(key)
            if val:
                try:
                    num = float(val)
                    if (min == None or num >= min) and \
                       (max == None or num <= max):
                        return num
                except ValueError:
                    pass
        print 'Option error - float key', key, 'is not valid'
        return 0

    def intData(self, key, min=None, max=None):
        """Return int from option data"""
        for data in self.dictList:
            val = data.get(key)
            if val:
                try:
                    num = int(val)
                    if (min == None or num >= min) and \
                       (max == None or num <= max):
                        return num
                except ValueError:
                    pass
        print 'Option error - int key', key, 'is not valid'
        return 0

    def strData(self, key, emptyOk=0):
        """Return string from option data"""
        for data in self.dictList:
            val = data.get(key)
            if val != None:
                if val or emptyOk:
                    return val
        print 'Option error - string key', key, 'is not valid'
        return ''

    def changeData(self, key, strData, storeChange):
        """Change entry, add to write list if storeChange
           Return true if changed"""
        for data in self.dictList:
            val = data.get(key)
            if val != None:
                if strData == val:  # no change reqd
                    return 0
                self.userDict[key] = strData
                if storeChange:
                    self.chgList.append(key)
                return 1
        print 'Option error - key', key, 'is not valid'
        return 0

    def writeChanges(self):
        """Write any stored changes to the option file - rtn true on success"""
        if self.path and self.chgList:
            try:
                f = codecs.open(self.path, 'r', 'utf-8')
                fileList = f.readlines()
                f.close()
                for key in self.chgList[:]:
                    hitList = [line for line in fileList if \
                               line.strip().split(None, 1)[:1] == [key]]
                    if not hitList:
                        hitList = [line for line in fileList if \
                                   line.replace('#', ' ', 1).strip().\
                                   split(None, 1)[:1] == [key]]
                    if hitList:
                        fileList[fileList.index(hitList[-1])] = '%s%s\n' % \
                                (key.ljust(self.keySpaces), self.userDict[key])
                        self.chgList.remove(key)
                for key in self.chgList:
                    fileList.append('%s%s\n' % (key.ljust(self.keySpaces), \
                                                self.userDict[key]))
                f = codecs.open(self.path, 'w', 'utf-8')
                f.writelines([line for line in fileList])
                f.close()
                return 1
            except IOError:
                print 'Error - could not write to config file', self.path
        return 0
