
import pyclbr   # parse a python module and describe its classes and methods
import pprint

misc_clbr = pyclbr.readmodule('lib.misc')
pprint.pprint(misc_clbr)

misc_clbr = pyclbr.readmodule('lib.nlp.wordnet.cache')
pprint.pprint(misc_clbr)
