import re

# based on:
#   http://immike.net/blog/2007/04/06/5-regular-expressions-every-web-programmer-should-know/
URL_RE = re.compile("""

  # Match the leading part (proto://hostname, or just hostname)
  (
    # http://, https:// or ftp leading part
    (ftp|https?)://[-\\w]+(\\.\\w[-\\w]*)+
  |
    # or, try to find a hostname with more specific sub-expression
    (?: [a-z0-9] (?:[-a-z0-9]*[a-z0-9])? \\. )+ # sub domains
    # Now ending .com, etc. For these, require lowercase
    (?: com\\b
        | edu\\b
        | biz\\b
        | gov\\b
        | int\\b
        | info\\b
        | mil\\b
        | net\\b
        | org\\b
        | [a-z][a-z]\\.[a-z][a-z]\\b # two-letter country code
    )
  )

  # Allow an optional port number
  ( : \\d+ )?

  # The rest of the URL is optional, and begins with /
  (
    /
    # The rest are heuristics for what seems to work well
    [^.!,?;"\\'<>()\[\]\{\}\s\x7F-\\xFF]*
    (
      [.!,?]+ [^.!,?;"\\'<>()\\[\\]\{\\}\s\\x7F-\\xFF]+
    )*
  )?
""", re.VERBOSE|re.IGNORECASE)


###
# Email validation patterns borrowed from:
#   http://www.regular-expressions.info/email.html

# very very general, probably too general.
RFC2822_RE = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", re.IGNORECASE)

# removing obsolete bracket notation
# EMAIL_I = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", re.IGNORECASE)

# refinment of EMAIL-I, it limits country code to 2 letters
EMAIL_RE = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum)", re.IGNORECASE)

# This pattern is more for validation
EMAIL_STRICT = re.compile('[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?:[A-Z]{2}|com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum)', re.IGNORECASE)
