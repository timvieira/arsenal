#!/usr/bin/env python
#
# PrettyTable 0.5
# Copyright (c) 2009, Luke Maurits <luke@maurits.id.au>
# All rights reserved.
# With contributions from:
#  * Chris Clark
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import copy
import sys

FRAME = 0
ALL   = 1
NONE  = 2

class PrettyTable:

    def __init__(self, fields=None, caching=True, padding_width=0, left_padding=None, right_padding=None):
        """
        fields - list or tuple of field names
        caching - boolean value to turn string caching on/off
        padding width - number of spaces between column lines and content
        """

        # Data
        self.fields = []
        if fields:
            self.set_field_names(fields)
        else:
            self.widths = []
            self.aligns = []
        self.padding_width = padding_width
        self.rows = []

        # Options
        self.hrules = FRAME
        self.caching = caching
        self.padding_width = padding_width
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.vertical_char = "|"
        self.horizontal_char = "="
        self.junction_char = "+"

    def __str__(self):
        return self.get_string()

    def set_field_names(self, fields):
        """ Set the names of the fields """
        # We *may* need to change the widths if this isn't the first time
        # setting the field names.  This could certainly be done more
        # efficiently.
        if self.fields:
            self.widths = [len(field) for field in fields]
            for row in self.rows:
                for i in xrange(len(row)):
                    if len(unicode(row[i])) > self.widths[i]:
                        self.widths[i] = len(unicode(row[i]))
        else:
            self.widths = [len(field) for field in fields]
        self.fields = fields
        self.aligns = len(fields)*["c"]

    def set_field_align(self, fieldname, align):
        """ Set the alignment of a field by its fieldname """
        if fieldname not in self.fields:
            raise Exception("No field %s exists!" % fieldname)
        if align not in ["l","c","r"]:
            raise Exception("Alignment %s is invalid, use l, c or r" % align)
        self.aligns[self.fields.index(fieldname)] = align

    def add_row(self, row):
        """
        Add a row to the table

        Arguments:
          row - row of data, should be a list with as many elements as the table
          has fields
        """
        if len(row) != len(self.fields):
            raise Exception("Row has incorrect number of values, (actual) %d!=%d (expected)" %(len(row),len(self.fields)))
        self.rows.append(row)
        for i in xrange(len(row)):
            if len(unicode(row[i])) > self.widths[i]:
                self.widths[i] = len(unicode(row[i]))

    def add_column(self, fieldname, column, align="c"):
        """
        Add a column to the table.

        Arguments:
          fieldname - name of the field to contain the new column of data
          column - column of data, should be a list with as many elements as the
          table has rows
          align - desired alignment for this column - "l" for left, "c" for centre and "r" for right
        """

        if len(self.rows) in (0, len(column)):
            if align not in ["l","c","r"]:
                raise Exception("Alignment %s is invalid, use l, c or r!" % align)
            self.fields.append(fieldname)
            self.widths.append(len(fieldname))
            self.aligns.append(align)
            for i in xrange(len(column)):
                if len(self.rows) < i+1:
                    self.rows.append([])
                self.rows[i].append(column[i])
                if len(unicode(column[i])) > self.widths[-1]:
                    self.widths[-1] = len(unicode(column[i]))
        else:
            raise Exception("Column length %d does not match number of rows %d!" % (len(column), len(self.rows)))

    def _get_sorted_rows(self, start, end, sortby, reversesort):
        # Sort rows using the "Decorate, Sort, Undecorate" (DSU) paradigm
        rows = copy.deepcopy(self.rows[start:end])
        sortindex = self.fields.index(sortby)
        # Decorate
        rows = [[row[sortindex]]+row for row in rows]
        # Sort
        rows.sort(reverse=reversesort)
        # Undecorate
        rows = [row[1:] for row in rows]
        return rows

    def _get_paddings(self):

        if self.left_padding is not None:
            lpad = self.left_padding
        else:
            lpad = self.padding_width
        if self.right_padding is not None:
            rpad = self.right_padding
        else:
            rpad = self.padding_width
        return lpad, rpad

    ##############################
    # ASCII PRINT/STRING METHODS #
    ##############################

    def printt(self, start=0, end=None, fields=None, header=True, border=True, hrules=FRAME, sortby=None, reversesort=False):
        """Print table in current state to stdout.

        Arguments:

        start - index of first data row to include in output
        end - index of last data row to include in output PLUS ONE (list slice style)
        fields - names of fields (columns) to include
        sortby - name of field to sort rows by
        reversesort - True or False to sort in descending or ascending order
        border - should be True or False to print or not print borders
        hrules - controls printing of horizontal rules after each row.  Allowed values: FRAME, ALL, NONE"""

        print self.get_string(start, end, fields, header, border, hrules, sortby, reversesort)

    def get_string(self, start=0, end=None, fields=None, header=True, border=True, hrules=FRAME, sortby=None, reversesort=False):
        """Return string representation of table in current state.

        Arguments:

        start - index of first data row to include in output
        end - index of last data row to include in output PLUS ONE (list slice style)
        fields - names of fields (columns) to include
        sortby - name of field to sort rows by
        reversesort - True or False to sort in descending or ascending order
        border - should be True or False to print or not print borders
        hrules - controls printing of horizontal rules after each row.  Allowed values: FRAME, ALL, NONE"""

        hrule = hrules or self.hrules
        bits = []
        if not self.fields:
            return ""
        if not header:
            # Recalculate widths - avoids tables with long field names but narrow data looking odd
            old_widths = self.widths[:]
            self.widths = [0]*len(self.fields)
            for row in self.rows:
                for i in xrange(len(row)):
                    if len(unicode(row[i])) > self.widths[i]:
                        self.widths[i] = len(unicode(row[i]))
        if header:
            bits.append(self._stringify_header(fields, border, hrules))
        elif border and hrules != NONE:
            bits.append(self._stringify_hrule(fields, border))
        if sortby:
            rows = self._get_sorted_rows(start, end, sortby, reversesort)
        else:
            rows = self.rows[start:end]
        for row in rows:
            bits.append(self._stringify_row(row, fields, border, hrule))
        if border and not hrule:
            bits.append(self._stringify_hrule(fields, border))
        string = "\n".join(bits)

        if not header:
            # Restore previous widths
            self.widths = old_widths
            for row in self.rows:
                for i in xrange(len(row)):
                    if len(unicode(row[i])) > self.widths[i]:
                        self.widths[i] = len(unicode(row[i]))
        return string

    def _stringify_hrule(self, fields=None, border=True):

        if not border:
            return ""
        lpad, rpad = self._get_paddings()
        padding_width = lpad+rpad
        bits = [self.junction_char]
        for field, width in zip(self.fields, self.widths):
            if fields and field not in fields:
                continue
            bits.append((width+padding_width)*self.horizontal_char)
            bits.append(self.junction_char)
        return "".join(bits)

    def _stringify_header(self, fields=None, border=True, hrules=FRAME):

        lpad, rpad = self._get_paddings()
        bits = []
        if border:
            if hrules != NONE:
                bits.append(self._stringify_hrule(fields, border))
                bits.append("\n")
            bits.append(self.vertical_char)
        for field, width in zip(self.fields, self.widths):
            if fields and field not in fields:
                continue
            bits.append(" " * lpad + field.center(width) + " " * rpad)
            if border:
                bits.append(self.vertical_char)
        if border and hrules != NONE:
            bits.append("\n")
            bits.append(self._stringify_hrule(fields, border))
        return "".join(bits)

    def _stringify_row(self, row, fields=None, border=True, hrule=False):

        lpad, rpad = self._get_paddings()
        bits = []
        if border:
            bits.append(self.vertical_char)
        for field, value, width, align in zip(self.fields, row, self.widths, self.aligns):
            if fields and field not in fields:
                continue
            if align == "l":
                bits.append(" " * lpad + unicode(value).ljust(width) + " " * rpad)
            elif align == "r":
                bits.append(" " * lpad + unicode(value).rjust(width) + " " * rpad)
            else:
                bits.append(" " * lpad + unicode(value).center(width) + " " * rpad)
            if border:
                bits.append(self.vertical_char)
        if border and hrule == ALL:
            bits.append("\n")
            bits.append(self._stringify_hrule(fields, border))
        return "".join(bits)


def main():

    x = PrettyTable(["City name", "Area", "Population", "Annual Rainfall"])
    x.set_field_align("City name", "l") # Left align city names
    x.add_row(["Adelaide",1295, 1158259, 600.5])
    x.add_row(["Brisbane",5905, 1857594, 1146.4])
    x.add_row(["Darwin", 112, 120900, 1714.7])
    x.add_row(["Hobart", 1357, 205556, 619.5])
    x.add_row(["Sydney", 2058, 4336374, 1214.8])
    x.add_row(["Melbourne", 1566, 3806092, 646.9])
    x.add_row(["Perth", 5386, 1554769, 869.4])
    print x

    if len(sys.argv) > 1 and sys.argv[1] == "test":

    # This "test suite" is hideous and provides poor, arbitrary coverage.
    # I'll replace it with some proper unit tests Sometime Soon (TM).
    # Promise.
        print "Testing field subset selection:"
        x.printt(fields=["City name","Population"])
        print "Testing row subset selection:"
        x.printt(start=2, end=5)
        print "Testing hrules settings:"
        print "FRAME:"
        x.printt(hrules=FRAME)
        print "ALL:"
        x.printt(hrules=ALL)
        print "NONE:"
        x.printt(hrules=NONE)
        print "Testing lack of headers:"
        x.printt(header=False)
        x.printt(header=False, border=False)
        print "Testing lack of borders:"
        x.printt(border=False)
        print "Testing sorting:"
        x.printt(sortby="City name")
        x.printt(sortby="Annual Rainfall")
        x.printt(sortby="Annual Rainfall", reversesort=True)
        print "Testing everything at once:"
        x.printt(start=2, end=5, fields=["City name","Population"], border=False, hrules=True)
        print "Rebuilding by columns:"
        x = PrettyTable()
        x.add_column("City name", ["Adelaide", "Brisbane", "Darwin", "Hobart", "Sydney", "Melbourne", "Perth"])
        x.add_column("Area", [1295, 5905, 112, 1357, 2058, 1566, 5385])
        x.add_column("Population", [1158259, 1857594, 120900, 205556, 4336374, 3806092, 1554769])
        x.add_column("Annual Rainfall", [600.5, 1146.4, 1714.7, 619.5, 1214.8, 646.9, 869.4])
        x.printt()
        print "Testing HTML:"
        x.print_html()
        x.print_html(border=False)
        x.print_html(border=True)
        x.print_html(format=False)
        x.print_html(attributes={"name": "table", "id": "table"})

if __name__ == "__main__":
    main()

