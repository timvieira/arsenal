"""
File system utilities
"""

import os
import tempfile

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

def atomicwrite(filename, contents, mode=0666):
    """Create a file 'filename' with 'contents' atomically.

    As in Write, 'mode' is modified by the umask.  This creates and moves
    a temporary file, and errors doing the above will be propagated normally,
    though it will try to clean up the temporary file in that case.

    This is very similar to the prodlib function with the same name.

    Args:
      filename: str; the name of the file
      contents: str; the data to write to the file
      mode: int; permissions with which to create the file (default is 0666 octal)
    """
    (fd, tmp_filename) = tempfile.mkstemp(prefix=filename,
                                          dir=os.path.dirname(filename))
    try:
        os.write(fd, contents)
    finally:
        os.close(fd)

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

import re
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

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you generate random
    filename if the function returned an empty one.
    """
    if isinstance(filename, unicode):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('ascii', 'ignore')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    filename = str(_filename_ascii_strip_re.sub('', '_'.join(
                   filename.split()))).strip('._')

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == 'nt' and filename and \
       filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename


# does not yet support finding directories
def find_files(d, filterfn=lambda x: True, relpath=True):
    """
    Recursively walks directory `d` yielding files which satisfy `filterfn`.
    Set option `relpath` to False to output absolute paths.
    """
    for dirpath, _, filenames in os.walk(d):
        for f in filenames:
            if relpath:
                f = os.path.join(dirpath, f)   # TIM: should I call abspath here?
            if filterfn(f):
                yield f


if __name__ == '__main__':
    import automain
    automain.automain()

