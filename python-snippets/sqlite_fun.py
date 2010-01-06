#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from sqlite3 import dbapi2 as sqlite

## TIP: you can use sqlite.connect(':memory:') for very fast in-memory stuff.

def create_db():
    # Create a database:
    con = sqlite.connect('mydatabase.db3')
    cur = con.cursor()
    
    # Create a table:
    cur.execute('create table clients (id INT PRIMARY KEY, name CHAR(60))')
    
    # Insert a single line:
    client = (5,"John Smith")
    cur.execute("insert into clients (id, name) values (?, ?)", client )
    con.commit()
    
    # Insert several lines at once:
    clients = [ (7,"Ella Fitzgerald"),
                (8,"Louis Armstrong"),
                (9,"Miles Davis")
              ]
    cur.executemany("insert into clients (id, name) values (?, ?)", clients )
    con.commit()
    
    cur.close()
    con.close()

'''
cur.executescript("""
    create table person(
        firstname,
        lastname,
        age
    );

    create table book(
        title,
        author,
        published
    );

    insert into book(title, author, published)
    values (
        'Dirk Gently''s Holistic Detective Agency',
        'Douglas Adams',
        1987
    );
    """)
'''

def example_query():
    # Connect to an existing database
    con = sqlite.connect('mydatabase.db3')
    cur = con.cursor()
    
    # Get row by row
    print "Row by row:"
    cur.execute('select id, name from clients order by name;')
    row = cur.fetchone()
    while row:
        print row
        row = cur.fetchone()
    
    # Get all rows at once:
    print "All rows at once:"
    cur.execute('select id, name from clients order by name;')
    print cur.fetchall()
    
    cur.close()
    con.close()


def mini_shell():
    """ A minimal SQLite shell for experiments """

    import sqlite3

    con = sqlite3.connect(":memory:")
    con.isolation_level = None
    cur = con.cursor()
    
    buf = ""
    
    print "Enter your SQL commands to execute in sqlite3."
    print "Enter a blank line to exit."
    
    while True:
        line = raw_input()
        if line == "":
            break
        buf += line
        if sqlite3.complete_statement(buf):
            try:
                buf = buf.strip()
                cur.execute(buf)
    
                if buf.lstrip().upper().startswith("SELECT"):
                    print cur.fetchall()
            except sqlite3.Error, e:
                print "An error occurred:", e.args[0]
            buf = ""
    
    con.close()
