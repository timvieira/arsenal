import pdb, sys
from functools import wraps
from misc import into_debugger

def main():
    x = 99
    1/0 

#assert into_debugger.__name__ == 'into_debugger'
#assert into_debugger(main).__name__ == 'main'
    
if __name__ == '__main__':
    if '--drop-into-debugger' in sys.argv:
        into_debugger(main)()
    else:
        main()

