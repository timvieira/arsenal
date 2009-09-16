# Based on:
#   Richard Jones' Log: Simple, elegant HTML generation 
#   <http://www.mechanicalcat.net/richard/log/Python/Simple__elegant_HTML_generation>

from cgi import escape

class HTML(object):
    """Easily generate HTML.

        >>> h = HTML()
        >>> p = h.p('hello, world!')
        >>> p.text('more text')
        >>> with h.table(border='1', newlines=True):
        ...     for i in range(2):
        ...         with h.tr:
        ...             h.td('he<l>lo', a='"foo"')
        ...             h.td('there')
        ... 
        >>> print h
        <p>hello, world!more text</p>
        <table border="1">
        <tr><td a="&quot;foo&quot;">he&lt;l&gt;lo</td><td>there</td></tr>
        <tr><td a="&quot;foo&quot;">he&lt;l&gt;lo</td><td>there</td></tr>
        </table>
    """
    def __init__(self, name=None, stack=None):
        self.name = name
        self.content = []
        self.attrs = {}
        # insert newlines between content?
        self.newlines = False
        if stack is None:
            stack = [self]
        self.stack = stack
    def __getattr__(self, name):
        # adding a new tag or newline
        if name == 'newline':
            e = '\n'
        else:
            e = HTML(name, self.stack)
        self.stack[-1].content.append(e)
        return e
    def text(self, text):
        # adding text
        self.content.append(escape(text))
    def __call__(self, *content, **kw):
        # customising a tag with content or attributes
        if content:
            self.content = map(escape, content)
        if 'newlines' in kw:
            # special-case to allow control over newlines
            self.newlines = kw.pop('newlines')
        for k in kw:
            self.attrs[k] = escape(kw[k], quote=True)
        return self
    def __enter__(self):
        # we're now adding tags to me!
        self.stack.append(self)
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        # we're done adding tags to me!
        self.stack.pop()
    def __str__(self):
        # turn me and my content into text
        sep = '\n' if self.newlines else ''
        if self.name is None:
            return sep.join(map(str, self.content))
        a = map('%s="%s"'.__mod__, self.attrs.iteritems())
        l = [self.name] + a
        s = '<%s>%s' % (' '.join(l), sep)
        if self.content:
            s += sep.join(map(str, self.content))
            s += sep + '</%s>'%self.name
        return s


if __name__ == '__main__':
    h = HTML()
    p = h.p('hello, world!')
    p.text('more text')
    with h.table(border='1', newlines=True):
        for i in range(2):
            with h.tr:
                h.td('he<l>lo', a='"foo"')
                h.td('there')
    print h

