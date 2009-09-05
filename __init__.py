##import iterextras
##import misc
##import LRU
##import lazy
##import datastructures
##
### experimental
##import BindingConstants
##
### Parsing stuff
##import BeautifulSoup
##import feedparser
##
### connecting
##import ftpserver
##import timeout_xmlrpclib
##
### systems
##import autoreload
##import path
##
### algorithms
##import weighted_choice
##import PorterStemmer
##import unionfind
##import bipartite_matching
##import combinatorics
##
### fun
##import termcolors
##import terminal_colors
##import gcal
##
##
### check if we've included everything in the directory
##from os import listdir
##for f in listdir('C:/projects/utils'):
##    if not f.startswith('__') and f.endswith('.py'):
##        module_name = f[:-3]
##        assert module_name in globals(), module_name + ' is not imported.'
##
