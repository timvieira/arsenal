import os
import inspect


def find_filename(obj):
    """Return the full filename of an instance. """

    if not isinstance(obj, basestring):
        
        # Return the name of the Python source file in which an object was defined. 
        # This will fail with a TypeError if the object is a built-in module, class,
        # or function.
        try:
            f = inspect.getsourcefile(obj)
        except TypeError:
            return None

    # don't visit *.pyc files
    f = os.path.splitext(f)
    if f[1] == ".pyc":
        f = (f[0], ".py")
    f = ''.join(f)

    if not os.path.isabs(f):
        f = os.path.join(os.getcwd(), f)

    if os.path.isfile(f):
        return f


def edit(obj):
    """
    Set the synchronize with editor hook with a callable object.
     - obj: introspection is used to retrieve relevant source code for the
       object; strings are treated as a filenames.
     - line : the line number to scroll to.
     - column : the column number to scroll to.
    """

    filename = find_filename(obj)
    if not filename:
        return

    try:
        # Return a list of source lines and starting line number for an object. 
        # The argument may be a module, class, method, function, traceback, frame,
        # or code object. The source code is returned as a list of the lines 
        # corresponding to the object and the line number indicates where in the 
        # original source file the first line of code was found. An IOError is raised
        # if the source code cannot be retrieved.
        _, line = inspect.getsourcelines(obj)
    except IOError:
        line = 0

    emacs(filename, line=line)


def emacs(filename, line=0, column=0):
    r = os.system('emacsclient -n +%d:%d "%s" 2>/dev/null' % (line, column, filename))
    if r != 0:
        os.system('emacs --quick -f server-start +%d:%d "%s"' % (line, column, filename))
    

if __name__ == '__main__':
    import alphabet
    edit(alphabet.Alphabet.__init__)

