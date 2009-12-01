from subprocess import Popen, PIPE

proc = Popen(['python','reverse.py'], shell=True, stdin=PIPE, stdout=PIPE)

for i in ('hello','hi','i love liver and cheese',''):
    proc.stdin.write('%s\r\n' % i)

while 1:
    out = proc.stdout.readline().rstrip()
    if out == '':
        break

    print 'output:', out




