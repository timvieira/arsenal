#!C:/Python25/python.exe
import os, SimpleXMLRPCServer

class Foo:
    def settings(self):
        return os.environ
    def echo(self, something):
        return something
    def greeting(self, name):
        return "hello, " + name
    def ls(self):
        return os.listdir('.')
    def test(self):
        return os.system('ls')

handler = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
handler.register_instance(Foo())
handler.handle_request()

