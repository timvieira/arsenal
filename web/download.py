import os
from urllib2 import urlopen
from fsutils import ensure_dir, secure_filename
from robust import timelimit, retry, TimeoutError

# TODO: add verbosity argument
# TODO: maybe store urls hierarchically like wget
# TODO: should maybe use a library function for this or just wget..
# TODO: adding a work queue and using mutli-threading seems like a decent idea..
def download(url, usecache=True, cachedir='cache~/', timeout=30, tries=3, pause=0.1, cachedonly=False):

    if cachedir:
        ensure_dir(cachedir)
        cached = os.path.join(cachedir, secure_filename(url))
    else:
        assert not usecache, 'must specify cachedir'

    # only return something for cached files
    if cachedonly:
        if not os.path.exists(cached):
            return

    if usecache and os.path.exists(cached):
        with file(cached) as f:
            return f.read()

    # use wget for ftp files
    if url.startswith('ftp'):

        # TODO: wget should probably write to a tmp file if there is no cache.
        assert usecache, 'ftp currently needs a cache..'

        retcode = os.system("wget '%s' -O '%s'" % (url, cached))
        if retcode != 0:
            if os.path.exists(cached):
                print 'download appears to have failed.. deleting file.'
                os.remove(cached)
                return

        with file(cached) as f:
            return f.read()

    @retry(tries=tries, pause=pause)
    @timelimit(timeout=timeout)
    def _download():
        try:
            with file(cached, 'wb') as f:
                x = urlopen(url).read()
                f.write(x)
                return x
        except:
            # delete file on failure
            if os.path.exists(cached):
                os.remove(cached)
            raise

    try:
        return _download()
    except TimeoutError:
        return
