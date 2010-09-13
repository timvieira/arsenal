"""
When you try to visit "http://cs.umass.edu/~mccallum" what happens behind the scenes?

Request path: /~mccallum from host: http://cs.umass.edu
  -> the host responses with a code 301 "Moved Permanently" and the new
     Location: "http://www.cs.umass.edu/~mccallum" in the header

As part of the its written in the RFC standards that 301 should be followed (should even be cached)

So we proceed to requesth /~mccallum from http://www.cs.umass.edu, we get a similar 301
but this time to http://www.cs.umass.edu/~mccallum/

We request the new path, /~mccallum/, and finally get a code 200 "OK"
"""

from urlparse import urlparse
from socket import socket, AF_INET, SOCK_STREAM
from StringIO import StringIO

def simple_get_url(url):
    """Request a URL in the most basic way."""
    u = urlparse(url)

    s = socket(AF_INET, SOCK_STREAM)  # create a TCP socket
    s.connect((u.hostname, 80))       # default http port is 80

    # send the http GET request
    s.send('GET %s HTTP/1.1\nHost: %s\n\n' % (u.path, u.hostname))

    # XXX: probably need to extract Content-length from header, but this seems to work fine.
    buf = StringIO()
    while True:
        line = s.recv(1024)
        if not line: break
        buf.write(line)
    return buf.getvalue()


if __name__ == '__main__':
    print simple_get_url('http://cs.umass.edu/~mccallum')

