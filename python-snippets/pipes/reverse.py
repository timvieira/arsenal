import sys

sys.stdout.write('reverser started\r\n')

line = None
while 1:
    line = sys.stdin.readline().rstrip()
    if not line:
        break
    sys.stdout.write('%s->%s\r\n' % (line, line.upper()))

sys.stdout.write('reverser is done...\r\n')

sys.stdout.flush()
