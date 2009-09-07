
import os
import re
import sys


def setup():
    """ Set-up some interactive features """

    __builtins__._H = [None]
    class Prompt:
        def __init__(self):
            self.str = '_H[%d]$ '    #'\001\033[0:1;31m\002h[%d] >>> \001\033[0m\002'
        def __str__(self):
            if hasattr(__builtins__, '_'):  # initially '_' this is not there.
                __builtins__._H.append(__builtins__._)
            return self.str % len(_H)
        def __radd__(self, other):
            return str(other) + str(self)

    class Prompt2:
        def __str__(self):
            return '.'*len(str(sys.ps1))
        def __radd__(self, other):
            return str(other) + str(self)

    sys.ps1 = Prompt()
    sys.ps2 = Prompt2()

    '''
    # LazyPython only works for Python versions 2.1 and above
    try:
        from LazyPython import LazyPython
        sys.excepthook = LazyPython()
    except ImportError:
        pass
    '''

    # Pretty-print at the command prompt for more readable dicts and lists.
    from pprint import pprint
    def my_displayhook(val):
        if val is not None:
            __builtins__._ = val
            pprint(val)
    sys.displayhook = my_displayhook


    # Try to set up command history completion, saving, and reloading
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        import rlcompleter
        readline.parse_and_bind("tab: complete")

        # The place to store your command history between sessions
        histfile = os.environ['HOME'] + '/.python-history'

        readline.read_history_file(histfile)

        import atexit       # read as "at exit"
        @atexit.register
        def savehist():
            try:
                readline.write_history_file(histfile)
            except:
                print 'Unable to save Python command history'


# SET IT UP!
setup()



'''

############################################################################
# Below this is Robin Friedrich's interactive.py with some edits to decrease 
# namespace pollution and change the help functionality
# NG
#
# Also enhanced 'which' to return filename/lineno
# Patch from Stephan Fiedler to allow multiple args to ls variants
# NG 10/21/01  --  Corrected a bug in _glob
#
########################### interactive.py ###########################
#  """Functions for doing shellish things in Python interactive mode.
#
#     Meant to be imported at startup via environment:
#       setenv PYTHONSTARTUP $HOME/easy.py
#       or
#       export PYTHONSTARTUP=$HOME/easy.py
#
#     - Robin Friedrich
#  """
import shutil
import glob
import os
import types
try:
    from pydoc import help
except ImportError:
    def help(*objects):
        """Print doc strings for object(s).
        Usage:  >>> help(object, [obj2, objN])  (brackets mean [optional] argument)
        """
        if len(objects) == 0:
            help(help)
            return
        for obj in objects:
            try:
                print '****', obj.__name__ , '****'
                print obj.__doc__
            except AttributeError:
                print `obj`, 'has no __doc__ attribute'
                print


home = os.path.expandvars('$HOME')

def _glob(filenames):
    """Expand a filename or sequence of filenames with possible
    shell metacharacters to a list of valid filenames.
    Ex:  _glob(('*.py*',)) == ['able.py','baker.py','charlie.py']
    """
    if type(filenames) is types.StringType:
        return glob.glob(filenames)
    flist = []
    for filename in filenames:
        globbed = glob.glob(filename)
        if globbed:
            for file in globbed:
                flist.append(file)
        else:
            flist.append(filename)
    return flist

def _expandpath(d):
    """Convert a relative path to an absolute path.
    """
    return os.path.join(os.getcwd(), os.path.expandvars(d))

def _ls(options, *files):
    """
    _ls(options, ['fname', ...'])

    Lists the given filenames, or the current directory if none are
    given, with the given options, which should be a string like '-lF'.
    """
    if len(files) == 0 :
        args = os.curdir
    else :
        args = ' '.join(files)
    os.system('ls %s %s' % (options, args))

def ls(*files):
    """Same as 'ls -aF'
    Usage:  >>> ls(['dirname', ...])   (brackets mean [optional]
argument)
    """
    _ls('-aF', *files)

def ll(*files):
    """Same as 'ls -alF'
    Usage:  >>> ll(['dirname', ...])   (brackets mean [optional]
argument)
    """
    _ls('-alF', *files)

def lr(*files):
    """Recursive listing. same as 'ls -aRF'
    Usage:  >>> lr(['dirname', ...])   (brackets mean [optional]
argument)
    """
    _ls('-aRF', *files)

mkdir = os.mkdir

def rm(*args):
    """Delete a file or files.
    Usage:  >>> rm('file.c' [, 'file.h'])  (brackets mean [optional] argument)
    Alias: delete
    """
    filenames = _glob(args)
    for item in filenames:
        try:
            os.remove(item)
        except os.error, detail:
            print "%s: %s" % (detail[1], item)
delete = rm

def rmdir(directory):
    """Remove a directory.
    Usage:  >>> rmdir('dirname')
    If the directory isn't empty, can recursively delete all sub-files.
    """
    try:
        os.rmdir(directory)
    except os.error:
        #directory wasn't empty
        answer = raw_input(directory+" isn't empty. Delete anyway?[n] ")
        if answer and answer[0] in 'Yy':
            os.system('rm -rf %s' % directory)
            print directory + ' Deleted.'
        else:
            print directory + ' Unharmed.'

def mv(*args):
    """Move files within a filesystem.
    Usage:  >>> mv('file1', ['fileN',] 'fileordir')
    If two arguments - both must be files
    If more arguments - last argument must be a directory
    """
    filenames = _glob(args)
    nfilenames = len(filenames)
    if nfilenames < 2:
        print 'Need at least two arguments'
    elif nfilenames == 2:
        try:
            os.rename(filenames[0], filenames[1])
        except os.error, detail:
            print "%s: %s" % (detail[1], filenames[1])
    else:
        for filename in filenames[:-1]:
            try:
                dest = filenames[-1]+'/'+filename
                if not os.path.isdir(filenames[-1]):
                    print 'Last argument needs to be a directory'
                    return
                os.rename(filename, dest)
            except os.error, detail:
                print "%s: %s" % (detail[1], filename)

def cp(*args):
    """Copy files along with their mode bits.
    Usage:  >>> cp('file1', ['fileN',] 'fileordir')
    If two arguments - both must be files
    If more arguments - last argument must be a directory
    """
    filenames = _glob(args)
    nfilenames = len(filenames)
    if nfilenames < 2:
        print 'Need at least two arguments'
    elif nfilenames == 2:
        try:
            shutil.copy(filenames[0], filenames[1])
        except os.error, detail:
            print "%s: %s" % (detail[1], filenames[1])
    else:
        for filename in filenames[:-1]:
            try:
                dest = filenames[-1]+'/'+filename
                if not os.path.isdir(filenames[-1]):
                    print 'Last argument needs to be a directory'
                    return
                shutil.copy(filename, dest)
            except os.error, detail:
                print "%s: %s" % (detail[1], filename)

def cpr(src, dst):
    """Recursively copy a directory tree to a new location
    Usage:  >>> cpr('directory0', 'newdirectory')
    Symbolic links are copied as links not source files.
    """
    shutil.copytree(src, dst)

def ln(src, dst):
    """Create a symbolic link.
    Usage:  >>> ln('existingfile', 'newlink')
    """
    os.symlink(src, dst)

def lnh(src, dst):
    """Create a hard file system link.
    Usage:  >>> ln('existingfile', 'newlink')
    """
    os.link(src, dst)

def pwd():
    """Print current working directory path.
    Usage:  >>> pwd()
    """
    print os.getcwd()

cdlist = [home]
def cd(directory = -1):
    """Change directory. Environment variables are expanded.
    Usage:
    cd('rel/$work/dir') change to a directory relative to your own
    cd('/abs/path')     change to an absolute directory path
    cd()                list directories you've been in
    cd(int)             integer from cd() listing, jump to that directory
    """
    global cdlist
    if type(directory) is types.IntType:
        if directory in range(len(cdlist)):
            cd(cdlist[directory])
            return
        else:
            pprint(cdlist)
            return
    directory = _glob(directory)[0]
    if not os.path.isdir(directory):
        print `directory`+' is not a directory'
        return
    directory = _expandpath(directory)
    if directory not in cdlist:
        cdlist.append(directory)
    os.chdir(directory)

def env():
    """List environment variables.
    Usage:  >>> env()
    """
    #unfortunately environ is an instance not a dictionary
    envdict = {}
    for key, value in os.environ.items():
        envdict[key] = value
    pprint(envdict)

interactive_dir_stack = []
def pushd(directory=home):
    """Place the current dir on stack and change directory.
    Usage:  >>> pushd(['dirname'])   (brackets mean [optional] argument)
                pushd()  goes home.
    """
    global interactive_dir_stack
    interactive_dir_stack.append(os.getcwd())
    cd(directory)

def popd():
    """Change to directory popped off the top of the stack.
    Usage:  >>> popd()
    """
    global interactive_dir_stack
    try:
        cd(interactive_dir_stack[-1])
        print interactive_dir_stack[-1]
        del interactive_dir_stack[-1]
    except IndexError:
        print 'Stack is empty'

def syspath():
    """Print the Python path.
    Usage:  >>> syspath()
    """
    import sys
    pprint(sys.path)

def which(object):
    """Print the source file from which a module, class, function, or method 
    was imported.
    
    Usage:    >>> which(mysteryObject)
    Returns:  Tuple with (file_name, line_number) of source file, or None if
              no source file exists
    Alias:    whence
    """
    object_type = type(object)
    if object_type is types.ModuleType:
        if hasattr(object, '__file__'):
            print 'Module from', object.__file__
            return (object.__file__, 1)
        else:
            print 'Built-in module.'
    elif object_type is types.ClassType:
        if object.__module__ == '__main__':
            print 'Built-in class or class loaded from $PYTHONSTARTUP'
        else:
            print 'Class', object.__name__, 'from', \
                    sys.modules[object.__module__].__file__
            # Send you to the first line of the __init__ method
            return (sys.modules[object.__module__].__file__, 
                    object.__init__.im_func.func_code.co_firstlineno)
    elif object_type in (types.BuiltinFunctionType, types.BuiltinMethodType):
        print "Built-in or extension function/method."
    elif object_type is types.FunctionType:
        print 'Function from', object.func_code.co_filename
        return (object.func_code.co_filename, object.func_code.co_firstlineno)
    elif object_type is types.MethodType:
        print 'Method of class', object.im_class.__name__, 'from', 
        fname = sys.modules[object.im_class.__module__].__file__
        print fname
        return (fname, object.im_func.func_code.co_firstlineno)
    else:
        print "argument is not a module or function."
    return None
whence = which

'''

