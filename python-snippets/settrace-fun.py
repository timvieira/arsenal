import sys


def trace_func(frame, event, arg):
    try:
        frame.f_locals['a'] = 'hacked(%s)' % (frame.f_locals["a"],)
    except KeyError as e:
        pass

def f(a):
    return a

if __name__ == '__main__':
    sys.settrace(trace_func)
    for i in range(0,5):
        print i, '=>', f(i)
