"""
import xmlrpclib

# Create an object to represent our server.
server_url = 'http://xmlrpc-c.sourceforge.net/api/sample.php';
server = xmlrpclib.Server(server_url);

# Call the server and get our result.
result = server.sample.sumAndDifference(5, 3)
print "Sum:", result['sum']
print "Difference:", result['difference']
"""


import xmlrpclib

server = xmlrpclib.ServerProxy("http://127.0.0.1/cgi-bin/cgi-rpc/rpc_server.py")


yoonikode = u'Sacr\xe9 Bleu'
tup = tuple([yoonikode])
print tup
textcall = xmlrpclib.dumps(tup,("server.echo"))
print 'Call:'
print textcall
print

print server.echo("hi")
print server.greeting("dilbert")
print server.greeting(yoonikode)
print '---------'
print server.ls()
print server.test()
