#!/usr/bin/python
import os, os.path, UserDict
from sqlite3 import dbapi2 as sqlite

class dbdict(UserDict.DictMixin):
    ''' dbdict, a persistent dictionnary-like object for large datasets '''

    def __init__(self,dictName):
        self.db_filename = "dbdict_%s.sqlite" % dictName
        if not os.path.isfile(self.db_filename):
            self.con = sqlite.connect(self.db_filename)
            self.con.execute("create table data (key PRIMARY KEY,value)")
        else:
            self.con = sqlite.connect(self.db_filename)

    def __getitem__(self, key):
        row = self.con.execute("select value from data where key=?",(key,)).fetchone()
        if not row: raise KeyError
        return row[0]

    def __setitem__(self, key, item):
        if self.con.execute("select key from data where key=?",(key,)).fetchone():
            self.con.execute("update data set value=? where key=?",(item,key))
        else:
            self.con.execute("insert into data (key,value) values (?,?)",(key, item))
        self.con.commit()

    def __delitem__(self, key):
        if self.con.execute("select key from data where key=?",(key,)).fetchone():
            self.con.execute("delete from data where key=?",(key,))
            self.con.commit()
        else:
             raise KeyError

    def keys(self):
        return [row[0] for row in self.con.execute("select key from data").fetchall()]


if __name__ == '__main__':

    d = dbdict("mydummydict")
    d["foo"] = "bar"

    # At this point, foo and bar are *written* to disk.
    d["John"] = "doh!"
    d["pi"] = 3.999
    d["pi"] = 3.14159

    # You can access your dictionnary later on:
    d = dbdict("mydummydict")
    del d["foo"]

    if "John" in d:
        print "John is in there !"
    print d.items()
