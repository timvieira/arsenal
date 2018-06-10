
from psutil import Process
from os import getpid


def memory_usage():
    "Return the memory usage of this process in MB."
    p = Process(getpid())
    return p.memory_info()[0] / 2**20


if __name__ == '__main__':
    print('memory usage: %.2f MB' % memory_usage())
