import linecache
import os
import tempfile

lorem = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
Vivamus eget elit. In posuere mi non risus. Mauris id quam posuere
lectus sollicitudin varius. Praesent at mi. Nunc eu velit. Sed augue
massa, fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
eros pede, egestas at, ultricies ac, pellentesque eu, tellus. 

Sed sed odio sed mi luctus mollis. Integer et nulla ac augue convallis
accumsan. Ut felis. Donec lectus sapien, elementum nec, condimentum ac,
interdum non, tellus. Aenean viverra, mauris vehicula semper porttitor,
ipsum odio consectetuer lorem, ac imperdiet eros odio a sapien. Nulla
mauris tellus, aliquam non, egestas a, nonummy et, erat. Vivamus
sagittis porttitor eros.'''

# Create a temporary text file with some text in it
fd, temp_file_name = tempfile.mkstemp()
os.close(fd)
with file(temp_file_name, 'wt') as f:
    f.write(lorem)

# Pick out the same line from source and cache.
# (Notice that linecache counts from 1)
print 'SOURCE: ', lorem.split('\n')[4]
print 'CACHE : ', linecache.getline(temp_file_name, 5).rstrip()

# Blank lines include the newline
print '\nBLANK : "%s"' % linecache.getline(temp_file_name, 6)

# The cache always returns a string, and uses an empty string to indicate
# a line which does not exist.
not_there = linecache.getline(temp_file_name, 500)
print '\nNOT THERE: "%s" includes %d characters' %  (not_there, len(not_there))

# Errors are even hidden if linecache cannot find the file
no_such_file = linecache.getline('this_file_does_not_exist.txt', 1)
print '\nNO FILE: ', no_such_file

# Look for the linecache module, using the built in sys.path search.
module_line = linecache.getline('linecache.py', 3)
print '\nMODULE : ', module_line


# Clean up
os.remove(temp_file_name)

