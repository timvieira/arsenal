import sys
import CGIHTTPServer
import BaseHTTPServer

assert __name__ != '__main__', 'This module should be run as a script.'

cgridirs = sys.argv[1:] or ["/cgi"]

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/cgi"]

PORT = 9999

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()
