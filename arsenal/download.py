import os
from arsenal.fsutils import mkdir, secure_filename
from arsenal.robust import timelimit, retry
from arsenal.misc import ignore_error
from urllib.request import Request, build_opener


def urlread(url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
                      ' AppleWebKit/525.13 (KHTML, like Gecko)'
                      ' Chrome/0.A.B.C Safari/525.13',
        'Referer': 'http://python.org'
    }

    request = Request(url, headers=req_headers)
    response = build_opener().open(request)

    code = response.code
    headers = response.headers
    contents = response.read()
    return code, headers, contents


def download(url, usecache=True, cached=None, cachedir='cache~/', cachedonly=False, **opts):
    """
    Download (or cache) ``url`` to file. On success: return file name of stored
    contents. Upon failure: return None.

    Will retry ``tries`` times with ``pause`` seconds between each attempt to
    download.

    Download will timeout after ``timeout`` seconds.

    If ``cachedonly`` is enabled, this function will not download anything. It
    will simply return the cached filename if it exists.
    """

    if not cached:
        if cachedir:
            mkdir(cachedir)
            cached = os.path.join(cachedir, secure_filename(url))
        else:
            assert not usecache, 'must specify cachedir'

    # only return something for cached files
    if cachedonly and not os.path.exists(cached):
        return

    if usecache and os.path.exists(cached):
        return cached

    # use wget for ftp files
    if url.startswith('ftp'):
        return wget(url, cached)

    if url.startswith('http'):
        return robust_download(url, cached, **opts)


def wget(url, filename):
    """
    Wraps call to wget to download ``url`` to ``filename``.
    """
    retcode = os.system("wget '%s' -O '%s'" % (url, filename))
    if retcode != 0:
        if os.path.exists(filename):
            os.remove(filename)
            return
    return filename


def robust_download(url, filename, tries=3, pause=0.1, timeout=30, verbose=True):
    """
    Attempts ``tries`` times to download and write contents ``url`` to
    ``filename``. Will timeout after ``timeout`` seconds.

    returns ``None`` upon failure and ``filename`` on success.
    """

    if verbose:
        print('trying to download %s to file://%s' % (url, filename))

    @retry(tries=tries, pause=pause)
    @timelimit(timeout)
    def _download():
        with open(filename, 'wb') as f:
            [code, _, contents] = urlread(url)
            assert code == 200
            f.write(contents)
            return filename

    result = None
    with ignore_error():
        result =_download()

    # delete file on failure
    if not result:
        if verbose: print('  failed to download')
        if os.path.exists(filename):
            if verbose: print('  deleting file')
            os.remove(filename)
        return
    else:
        if verbose: print('  download successful')
        return filename


if __name__ == '__main__':
    download('http://timvieira.github.com', cachedir='/tmp/')
