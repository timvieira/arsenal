import re, os
from urllib2 import urlopen
from fsutils import ensure_dir
#from urlparse import urlparse

def download(url, usecached=True, cachedir='cache/'):
    ensure_dir(cachedir)

    # TODO: handle ftp, http, etc
    #if urlparse(url).scheme.startswith('http')

    ensure_dir(cachedir)

    cached = cachedir + '/' + url.replace('/','#')   # TODO: store urls like wget
    if usecached and os.path.exists(cached):
        with file(cached) as f:
            return f.read()

    try:
        with file(cached, 'wb') as f:
            x = urlopen(url).read()
            f.write(x)
            return x
    except:
        if os.path.exists(cached):
            os.remove(cached)
        raise

