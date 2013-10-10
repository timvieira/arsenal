"""
The module is a wrapper for the Python Standard Library xmlrpclib, which makes
it very easy to set a timeout on a connecting and communicating with an xmlrpc
server.

usage:
    >>> from timeout_xmlrpclib import Server
    >>> server = Server('http://localhost:8080',timeout=30)
"""

import xmlrpclib, httplib

class TimeoutTransport(xmlrpclib.Transport):
    def make_connection(self, host):
        conn = TimeoutHTTP(host)
        conn.set_timeout(self.timeout)
        return conn

class TimeoutHTTPConnection(httplib.HTTPConnection):
    def connect(self):
         httplib.HTTPConnection.connect(self)
         self.sock.settimeout(self.timeout)

class TimeoutHTTP(httplib.HTTP):
    _connection_class = TimeoutHTTPConnection
    def set_timeout(self, timeout):
         self._conn.timeout = timeout

def Server(url, *args, **kwargs):
    t = TimeoutTransport()
    t.timeout = kwargs.pop('timeout', 20)
    kwargs['transport'] = t
    server = xmlrpclib.Server(url, *args, **kwargs)
    return server
