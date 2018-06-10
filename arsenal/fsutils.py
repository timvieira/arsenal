"""
File system utilities
"""
import re, os, tempfile, shutil
from contextlib import contextmanager
from fnmatch import fnmatch
from arsenal.iterextras import atmost
from subprocess import Popen, PIPE
from path import Path


def filesize(f):
    """
    Uses du to compute human readable summary of filesize.

    It's a wrapper around

    $ du -hs filename

    """
    f = Path(f)
    if not f.exists():
        return 'unknown'
    try:
        return Popen(['du', '-hs', f], stdout=PIPE).communicate()[0].strip().split()[0]
    except TypeError:
        return 'unknown'


def filetype(f):
    try:
        return Popen(['file', '-ib', f], stdout=PIPE).communicate()[0].split(';')[0]
    except TypeError:
        return 'unknown'


def mkdir(d, verbose=False):
    """ Ensure  directories need to create a file exist. """
    try:
        os.makedirs(d)
    except OSError as e:
        if verbose:
            print('[ensuredir]', d, 'suppressing:', e)
        if e.errno != 17:  # errno 17: File exists (you probably don't have permissions)
            raise
    else:
        if verbose:
            print('[ensuredir] created', d)
    return d


def ensure_dir(f, verbose=False):
    """ Ensure  directories need to create a file exist. """
    d = os.path.abspath(os.path.dirname(f))
    mkdir(d, verbose=verbose)
    return d


def clear_dir(d):
    try:
        shutil.rmtree(d)
    except:
        pass
    os.mkdir(d)


@contextmanager
def cd(d=None):
    before = os.getcwd()
    if d is not None:
        os.chdir(d)
    yield
    os.chdir(before)


class preserve_cwd(object):
    """
    context-manager which doubles as a decorator that preserve current
    working directory.

    Usage example:

    As a decorator:
        >>> before = os.getcwd()
        >>> @preserve_cwd
        ... def foo():
        ...     os.chdir('..')
        >>> foo()
        >>> before == os.getcwd()
        True

    As a context-manager:
        >>> before = os.getcwd()
        >>> with preserve_cwd():
        ...     os.chdir('..')
        >>> before == os.getcwd()
        True
    """
    def __init__(self, f=None):
        self.f = f
        self._cwd = None

    def __enter__(self):
        self._cwd = os.getcwd()

    def __exit__(self, *args):
        os.chdir(self._cwd)

    def __call__(self, *args, **kwargs):
        with self:
            return self.f(*args, **kwargs)


@contextmanager
def atomicwrite(filename, mode=0o666, verbose=False):
    """
    Write to `filename` atomically, if for some reason an error occurs in this
    context the contents of the file prior to entering will not be lost.

    Args:
      filename: str; the name of the file
      mode: permissions with which to create the file
    """

    # create the temp file in the same directory
    _, tmp_filename = tempfile.mkstemp(prefix=os.path.basename(filename),
                                       dir=os.path.dirname(filename))

    if verbose:
        print('[atomicwrite] using temporary file:', tmp_filename)

    with open(tmp_filename, 'wb') as f:
        yield f

    try:
        os.chmod(tmp_filename, mode)
        os.rename(tmp_filename, filename)
    except OSError as exc:
        try:
            os.remove(tmp_filename)
        except OSError as e:
            exc = OSError('%s.\n\natomicwrite encountered additional '
                          'errors cleaning up temporary file "%s":\n%s' % (exc, tmp_filename, e))
        raise exc


_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')
_windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                         'LPT2', 'LPT3', 'PRN', 'NUL')

def secure_filename(filename):
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    On windows system the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename(u'i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'
    >>> secure_filename(u'no brackets [ ] allowed either.txt')
    'no_brackets___allowed_either.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you generate random
    filename if the function returned an empty one.
    """
    if isinstance(filename, str):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    filename = str(_filename_ascii_strip_re.sub('', '_'.join(
                   filename.split()))).strip('._')
    filename = re.sub('[\[\]]', '', filename)

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == 'nt' and filename and \
       filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename


def find_new_title(d, filename):
    """If file *filename* exists in directory `d`, adds or changes the
    end of the file title until a name is found that doesn't yet exist.
    Returns the new file name (without directory).
    For instance, if file "Image (01).jpg" exists,
    returns "Image (02).jpg".
    """
    rx = re.compile(r"\((\d{1,5})\)$")
    p = os.path.join(d, filename)
    while os.path.exists(p):
        base = os.path.basename(p)
        (root, ext) = os.path.splitext(base)
        m = rx.search(root)
        if m == None:
            replacement = "(001)"
        else:
            increment = int(m.group(1)) + 1
            replacement = "(%03d)" % increment
            root = root[:m.start(1)-1]
        f = root + replacement + ext
        p = os.path.join(d, f)
    return p


def files(d, abspath=False):
    "Recursively list all files."
    for dirpath, _, filenames in os.walk(d):
        for f in filenames:
            f = os.path.join(dirpath, f)
            if abspath:
                f = os.path.abspath(f)
            yield f


# TODO: there has to be a faster way to do this which doesn't
# require reading a list of all the files in the directory.
def directories(d, abspath=False):
    """ recursively list all directories. """
    for directory, _, _ in os.walk(d):
        if abspath:
            directory = os.path.abspath(directory)
        yield directory


def find(d, filterfn=None, abspath=False, glob=None, regex=None, dirs=False):
    """
    Recursively walks directory `d` yielding files which satisfy `filterfn`.
    Set option `relpath` to False to output absolute paths.

    glob: shell glob filter function
    regex: regex filter function
    dirs: only search for directories matching filterfn
    """

    assert atmost(1, [filterfn, glob, regex])

    if filterfn is None:
        if glob is not None:
            filterfn = lambda x: fnmatch(x, glob)
        elif regex is not None:
            filterfn = re.compile(regex).match

    collection = directories(d, abspath=abspath) if dirs else files(d, abspath=abspath)

    for item in collection:
        if filterfn is None or filterfn(item):
            yield item


if __name__ == '__main__':

    def run_tests():

        def test_preserve_cwd():
            before = os.getcwd()
            with preserve_cwd():
                os.chdir('..')
                os.chdir('..')
            assert before == os.getcwd()

            @preserve_cwd
            def foo():
                os.chdir('..')
                os.chdir('..')
            cwd_before = os.getcwd()
            foo()
            assert os.getcwd() == cwd_before

        test_preserve_cwd()
        print('done.')

    run_tests()
