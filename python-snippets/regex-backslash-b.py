import re

print re.findall("\\b([A-Z])\\b", "A B bCb D")
print ['A', 'B', 'D']
print

# equivalent to the previous, but easier on the eyes
print re.findall(r"\b([A-Z])\b", "A B bCb D")
print ['A', 'B', 'D']
print

# other escapes .. whats the deal...
print re.findall("\\b([A-Z])\\b\s", "A B bCb D")
print ['A', 'B']
print

# \s can be double escaped!
print re.findall("\\b([A-Z])\\b\\s", "A B bCb D")
print ['A', 'B']
print

# using raw strings makes your regex look nicer!
print re.findall(r"\b([A-Z])\b\s", "A B bCb D")
print ['A', 'B']
print


# Other notes:

# Here it will match the \b escape character
print re.findall("\b([A-Z])\b", "A B \bC\b D")
print ['C']
print

# Note: '\b' is a valid word boundary character around 'C'
print re.findall(r"\b([A-Z])\b", "A B \bC\b D")
print ['A', 'B', 'C', 'D']
print

# \b is some special escape code (see it disappear)
print "\b([A-Z])\b"
print '([A-Z])'
