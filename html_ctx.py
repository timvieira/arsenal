# Copyright (c) 2009 eKit.com Inc (http://www.ekit.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Simple, elegant HTML generation.

Constructing your HTML
----------------------

To construct HTML start with an instance of ``html.HTML()``. Add
tags by accessing the tag's attribute on that object. For example::

   >>> from html_ctx import HTML
   >>> h = HTML()
   >>> print h.br
   <br>

If the tag should have text content you may pass it at tag creation time or
later using the tag's ``.text()`` method (note it is assumed that a fresh
``HTML`` instance is created for each of the following examples)::

   >>> p = h.p('hello, world! & ')
   >>> p.text('more &rarr; text', escape=False)
   >>> print p            #doctest:+NORMALIZE_WHITESPACE
   <p>hello, world! &amp; more &rarr; text</p>

Any HTML-specific characters (``<>&"``) in the text will be escaped for HTML
safety as appropriate unless ``escape=False`` is passed. Note also that the
top-level ``HTML`` object adds newlines between tags by default.

If the tag should have sub-tags you have two options. You may either add
the sub-tags directly on the tag::

   >>> l = h.ol
   >>> l.li('item 1')
   <HTML li>
   >>> l.li.b('item 2 > 1')
   <HTML b>
   >>> print h
   <br>
   <p>hello, world! &amp; more &rarr; text</p>
   <ol>
   <li>item 1</li>
   <li><b>item 2 &gt; 1</b></li>
   </ol>

Note that the default behavior with lists (and tables) is to add newlines
between sub-tags to generate a nicer output. You can also see in that
example the chaining of tags in ``l.li.b``. If you wished you could add
attributes to those chained tags, eg: ``l.li(id="special").b``.

The alternative to the above method is to use the containter tag as a
context for adding the sub-tags. The top-level ``HTML`` object keeps track
of which tag is the current context::

   >>> h = HTML()
   >>> with h.table(border='1'):
   ...     for i in range(2):
   ...         with h.tr:
   ...             h.td('column 1')
   ...             h.td('column 2')
   ...
   >>> print h
   <table border="1">
   <tr><td>column 1</td><td>column 2</td></tr>
   <tr><td>column 1</td><td>column 2</td></tr>
   </table>

Note the addition of an attribute to the ``<table>`` tag.

A variation on the above is to explicitly reference the context variable,
but then there's really no benefit to using a ``with`` statement. The
following is functionally identical to the first list construction::

   >>> with h.ol as l:
   ...     l.li('item 1')
   ...     l.li.b('item 2 > 1')
   ...

You may turn off/on adding newlines by passing ``newlines=False`` or
``True`` to the tag (or ``HTML`` instance) at creation time::

   >>> h = HTML()
   >>> l = h.ol(newlines=False)
   >>> l.li('item 1')
   >>> l.li('item 2')
   >>> print h
   <ol><li>item 1</li><li>item 2</li></ol>

Since we can't use ``class`` as a keyword, the library recognises ``klass``
as a substitute::

   >>> print h.p('content', klass="styled")
   <p class="styled">content</p>


How generation works
--------------------

The HTML document is generated when the ``HTML`` instance is "stringified".
This could be done either by invoking ``str()`` on it, or just printing it.

You may also render any tag or sub-tag at any time by stringifying it.

Tags with no contents (either text or sub-tags) will have no closing tag.
There is no "special list" of tags that must always have closing tags, so
if you need to force a closing tag you'll need to provide some content,
even if it's just a single space character.

Rendering doesn't affect the HTML document's state, so you can add to or
otherwise manipulate the HTML after you've stringified it.

----

This code is copyright 2009 eKit.com Inc (http://www.ekit.com/)
See the end of the source file for the license of use.
"""

__version__ = '1.4'

import unittest
import cgi

class HTML(object):
    """ Easily generate HTML. """
    newline_default_on = set('table ol ul dl'.split())

    def __init__(self, name=None, stack=None, newlines=True):
        self.name = name
        self.content = []
        self.attrs = {}
        # insert newlines between content?
        if stack is None:
            stack = [self]
            self.top = True
            self.newlines = newlines
        else:
            self.top = False
            self.newlines = name in self.newline_default_on
        self.stack = stack
    def __getattr__(self, name):
        # adding a new tag or newline
        if name == 'newline':
            e = '\n'
        else:
            e = HTML(name, self.stack)
        if self.top:
            self.stack[-1].content.append(e)
        else:
            self.content.append(e)
        return e
    def text(self, text, escape=True):
        if escape:
            text = cgi.escape(text)
        # adding text
        if self.top:
            self.stack[-1].content.append(text)
        else:
            self.content.append(text)
    def __call__(self, *content, **kw):
        # customising a tag with content or attributes
        if content:
            self.content = map(cgi.escape, content)
        if 'newlines' in kw:
            # special-case to allow control over newlines
            self.newlines = kw.pop('newlines')
        for k in kw:
            if k == 'klass':
                self.attrs['class'] = cgi.escape(kw[k], True)
            else:
                self.attrs[k] = cgi.escape(kw[k], True)
        return self
    def __enter__(self):
        # we're now adding tags to me!
        self.stack.append(self)
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        # we're done adding tags to me!
        self.stack.pop()
    def __repr__(self):
        return '<HTML %s>' % (self.name)
    def __str__(self):
        # turn me and my content into text
        join = '\n' if self.newlines else ''
        if self.name is None:
            return join.join(map(str, self.content))
        a = ['%s="%s"'%i for i in self.attrs.items()]
        l = [self.name] + a
        s = '<%s>%s'%(' '.join(l), join)
        if self.content:
            s += join.join(map(str, self.content))
            s += join + '</%s>'%self.name
        return s

class TestCase(unittest.TestCase):
    def test_empty_tag(self):
        'generation of an empty tag'
        h = HTML()
        h.br
        self.assertEquals(str(h), '<br>')

    def test_just_tag(self):
        'generate the HTML for just one tag'
        h = HTML()
        h.br
        self.assertEquals(str(h.br), '<br>')

    def test_para_tag(self):
        'generation of a tag with contents'
        h = HTML()
        h.p('hello')
        self.assertEquals(str(h), '<p>hello</p>')

    def test_escape(self):
        'escaping of special HTML characters in text'
        h = HTML()
        h.text('<>&')
        self.assertEquals(str(h), '&lt;&gt;&amp;')

    def test_no_escape(self):
        'no escaping of special HTML characters in text'
        h = HTML()
        h.text('<>&', False)
        self.assertEquals(str(h), '<>&')

    def test_escape_attr(self):
        'escaping of special HTML characters in attributes'
        h = HTML()
        h.a(a='<>&"')
        self.assertEquals(str(h), '<a a="&lt;&gt;&amp;&quot;">')

    def test_subtag_context(self):
        'generation of sub-tags using "with" context'
        h = HTML()
        with h.ol:
            h.li('foo')
            h.li('bar')
        self.assertEquals(str(h), '<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>')

    def test_subtag_direct(self):
        'generation of sub-tags directly on the parent tag'
        h = HTML()
        l = h.ol
        l.li('foo')
        l.li.b('bar')
        self.assertEquals(str(h), '<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>')

    def test_subtag_direct_context(self):
        'generation of sub-tags directly on the parent tag in "with" context'
        h = HTML()
        with h.ol as l:
            l.li('foo')
            l.li.b('bar')
        self.assertEquals(str(h), '<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>')

    def test_subtag_no_newlines(self):
        'prevent generation of newlines against default'
        h = HTML()
        l = h.ol(newlines=False)
        l.li('foo')
        l.li('bar')
        self.assertEquals(str(h), '<ol><li>foo</li><li>bar</li></ol>')

    def test_add_text(self):
        'add text to a tag'
        h = HTML()
        p = h.p('hello, world!\n')
        p.text('more text')
        self.assertEquals(str(h), '<p>hello, world!\nmore text</p>')

    def test_add_text_newlines(self):
        'add text to a tag with newlines for prettiness'
        h = HTML()
        p = h.p('hello, world!', newlines=True)
        p.text('more text')
        self.assertEquals(str(h), '<p>\nhello, world!\nmore text\n</p>')

    def test_doc_newlines(self):
        'default document adding newlines between tags'
        h = HTML()
        h.br
        h.br
        self.assertEquals(str(h), '<br>\n<br>')

    def test_doc_no_newlines(self):
        'prevent document adding newlines between tags'
        h = HTML(newlines=False)
        h.br
        h.br
        self.assertEquals(str(h), '<br><br>')

    def test_table(self):
        'multiple "with" context blocks'
        h = HTML()
        with h.table(border='1'):
            for i in range(2):
                with h.tr:
                    h.td('column 1')
                    h.td('column 2')
        self.assertEquals(str(h), '''<table border="1">
<tr><td>column 1</td><td>column 2</td></tr>
<tr><td>column 1</td><td>column 2</td></tr>
</table>''')


if __name__ == '__main__':
    unittest.main()
