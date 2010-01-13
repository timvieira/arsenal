from os.path import join, abspath, basename, exists
import wordnet_data

def find(resource_name):
    wn = abspath(wordnet_data.__path__[0])
    f  = basename(resource_name)
    p  = join(wn, f)
    if exists(p):
        return p
    raise LookupError("Resource: %s not found." % resource_name)

