"""
File system utilities
"""

import os
import tempfile

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

