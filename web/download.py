import os, socket, random
from fsutils import ensure_dir, secure_filename
from robust import timelimit, retry, TimeoutError
from misc import ignore_error

#use hacked user-agent instead
#from urllib2 import urlopen

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

import urllib2

def get_url(url):
    '''get_url accepts a URL string and return the server response code, response headers, and contents of the file'''

    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13',
        'Referer': 'http://python.org'
    }

    request = urllib2.Request(url, headers=req_headers) # create a request object for the URL
    opener = urllib2.build_opener() # create an opener object
    response = opener.open(request) # open a connection and receive the http response headers + contents

    code = response.code
    headers = response.headers # headers object
    contents = response.read() # contents of the URL (HTML, javascript, css, img, etc.)
    return code, headers, contents



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
                os.remove(cached)
                return

        with file(cached) as f:
            return f.read()

    @retry(tries=tries, pause=pause)
    @timelimit(timeout=timeout)
    def _download():
        with file(cached, 'wb') as f:
            [code, _, contents] = get_url(url)
            assert code == 200
            f.write(contents)
            return contents

    content = None
    with ignore_error():
        content = _download()

    if not content:
        # delete file on failure
        if os.path.exists(cached):
            os.remove(cached)
