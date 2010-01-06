import paramiko
from terminal_colors import blue, red, black

ssh = None

def connect():
    print 'connecting...'
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('jasper.cs.umass.edu', username='timv')
    return ssh

def run(cmd):
    s = ssh or connect()
    stdin, stdout, stderr = s.exec_command(cmd)
    blue()
    print ''.join(stdout.readlines()).strip()
    red()
    print ''.join(stderr.readlines()).strip()
    black()
    if stdin.channel.closed:
        return None
    return stdin

