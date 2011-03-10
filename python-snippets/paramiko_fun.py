from paramiko import SSHClient, AutoAddPolicy
from terminal.colors import blue, red, black

class SSH(object):

    def __init__(self, host, user):
        c = SSHClient()
        c.set_missing_host_key_policy(AutoAddPolicy())  # try to use automatic authentication
        c.connect(host, username=user)
        self.connection = c

    def run(self, cmd):
        stdin, stdout, stderr = self.connection.exec_command(cmd)
        print blue % (''.join(stdout.readlines()).strip(),)
        print red % (''.join(stderr.readlines()).strip())


def run(cmd, host='jasper.cs.umass.edu', user='timv'):
    c = SSH(host=host, user=user)
    c.run(cmd)
