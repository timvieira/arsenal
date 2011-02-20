import sys
import CGIHTTPServer
import BaseHTTPServer

assert __name__ != '__main__', 'This module should be run as a script.'

cgridirs = sys.argv[1:] or ["/cgi"]

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/cgi"]

def serve(port=9999):
    httpd = BaseHTTPServer.HTTPServer(("", port), Handler)
    print "serving at port", port
    httpd.serve_forever()

if __name__ == '__main__':
    serve()
