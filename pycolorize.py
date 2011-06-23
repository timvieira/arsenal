#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Class and program to colorize python source code for ANSI terminals.

Based on an HTML code highlighter by Jurgen Hermann found at:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52298

Modifications by Fernando Perez (fperez@colorado.edu).

Information on the original HTML highlighter follows:

MoinMoin - Python Source Parser

Title: Colorize Python source using the built-in tokenizer

Submitter: Jurgen Hermann
Last Updated:2001/04/06

Version no:1.2

Description:

This code is part of MoinMoin (http://moin.sourceforge.net/) and converts
Python source code to HTML markup, rendering comments, keywords,
operators, numeric and string literals in different colors.

It shows how to use the built-in keyword, token and tokenize modules to
scan Python source code and re-emit it with no changes to its original
formatting (which is the hard part).
"""

__all__ = ['ANSICodeColors','Parser']

_scheme_default = 'LightBG'

# Imports
import cStringIO
import keyword
import os
import optparse
import string
import sys
import token
import tokenize

import os

def make_color_table(in_class):
    """Build a set of color attributes in a class.

    Helper function for building the *TermColors classes."""
    
    color_templates = (
        # Dark colors
        ("Black"       , "0;30"),
        ("Red"         , "0;31"),
        ("Green"       , "0;32"),
        ("Brown"       , "0;33"),
        ("Blue"        , "0;34"),
        ("Purple"      , "0;35"),
        ("Cyan"        , "0;36"),
        ("LightGray"   , "0;37"),
        # Light colors
        ("DarkGray"    , "1;30"),
        ("LightRed"    , "1;31"),
        ("LightGreen"  , "1;32"),
        ("Yellow"      , "1;33"),
        ("LightBlue"   , "1;34"),
        ("LightPurple" , "1;35"),
        ("LightCyan"   , "1;36"),
        ("White"       , "1;37"),  
        # Blinking colors.  Probably should not be used in anything serious.
        ("BlinkBlack"  , "5;30"),
        ("BlinkRed"    , "5;31"),
        ("BlinkGreen"  , "5;32"),
        ("BlinkYellow" , "5;33"),
        ("BlinkBlue"   , "5;34"),
        ("BlinkPurple" , "5;35"),
        ("BlinkCyan"   , "5;36"),
        ("BlinkLightGray", "5;37"),
        )

    for name,value in color_templates:
        setattr(in_class,name,in_class._base % value)

class TermColors:
    """Color escape sequences.

    This class defines the escape sequences for all the standard (ANSI?) 
    colors in terminals. Also defines a NoColor escape which is just the null
    string, suitable for defining 'dummy' color schemes in terminals which get
    confused by color escapes.

    This class should be used as a mixin for building color schemes."""
    
    NoColor = ''  # for color schemes in color-less terminals.
    Normal = '\033[0m'   # Reset normal coloring
    _base  = '\033[%sm'  # Template for all other colors

# Build the actual color table as a set of class attributes:
make_color_table(TermColors)

class InputTermColors:
    """Color escape sequences for input prompts.

    This class is similar to TermColors, but the escapes are wrapped in \001
    and \002 so that readline can properly know the length of each line and
    can wrap lines accordingly.  Use this class for any colored text which
    needs to be used in input prompts, such as in calls to raw_input().

    This class defines the escape sequences for all the standard (ANSI?) 
    colors in terminals. Also defines a NoColor escape which is just the null
    string, suitable for defining 'dummy' color schemes in terminals which get
    confused by color escapes.

    This class should be used as a mixin for building color schemes."""
    
    NoColor = ''  # for color schemes in color-less terminals.

    if os.name == 'nt' and os.environ.get('TERM','dumb') == 'emacs':
        # (X)emacs on W32 gets confused with \001 and \002 so we remove them
        Normal = '\033[0m'   # Reset normal coloring
        _base  = '\033[%sm'  # Template for all other colors
    else:
        Normal = '\001\033[0m\002'   # Reset normal coloring
        _base  = '\001\033[%sm\002'  # Template for all other colors

# Build the actual color table as a set of class attributes:
make_color_table(InputTermColors)

class ColorScheme:
    """Generic color scheme class. Just a name and a Struct."""
    def __init__(self,__scheme_name_,colordict=None,**colormap):
        self.name = __scheme_name_
        if colordict is None:
            #self.colors = Struct(**colormap)
	    self.colors = dict(**colormap)
        else:
            #self.colors = Struct(colordict)
            self.colors = dict(colordict)

    def copy(self,name=None):
        """Return a full copy of the object, optionally renaming it."""
        if name is None:
            name = self.name
        return ColorScheme(name,self.colors.__dict__)
        
class ColorSchemeTable(dict):
    """General class to handle tables of color schemes.

    It's basically a dict of color schemes with a couple of shorthand
    attributes and some convenient methods.
    
    active_scheme_name -> obvious
    active_colors -> actual color table of the active scheme"""

    def __init__(self,scheme_list=None,default_scheme=''):
        """Create a table of color schemes.

        The table can be created empty and manually filled or it can be
        created with a list of valid color schemes AND the specification for
        the default active scheme.
        """
        
        # create object attributes to be set later
        self.active_scheme_name = ''
        self.active_colors = None
        
        if scheme_list:
            if default_scheme == '':
                raise ValueError,'you must specify the default color scheme'
            for scheme in scheme_list:
                self.add_scheme(scheme)
            self.set_active_scheme(default_scheme)

    def copy(self):
        """Return full copy of object"""
        return ColorSchemeTable(self.values(),self.active_scheme_name)

    def add_scheme(self,new_scheme):
        """Add a new color scheme to the table."""
        if not isinstance(new_scheme,ColorScheme):
            raise ValueError,'ColorSchemeTable only accepts ColorScheme instances'
        self[new_scheme.name] = new_scheme
        
    def set_active_scheme(self,scheme,case_sensitive=0):
        """Set the currently active scheme.

        Names are by default compared in a case-insensitive way, but this can
        be changed by setting the parameter case_sensitive to true."""

        scheme_names = self.keys()
        if case_sensitive:
            valid_schemes = scheme_names
            scheme_test = scheme
        else:
            valid_schemes = [s.lower() for s in scheme_names]
            scheme_test = scheme.lower()
        try:
            scheme_idx = valid_schemes.index(scheme_test)
        except ValueError:
            raise ValueError,'Unrecognized color scheme: ' + scheme + \
                  '\nValid schemes: '+str(scheme_names).replace("'', ",'')
        else:
            active = scheme_names[scheme_idx]
            self.active_scheme_name = active
            self.active_colors = self[active].colors
            # Now allow using '' as an index for the current active scheme
            self[''] = self[active]



#############################################################################
### Python Source Parser (does Hilighting)
#############################################################################

_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2

#****************************************************************************
# Builtin color schemes

Colors = TermColors  # just a shorthand

# Build a few color schemes
NoColor = ColorScheme(
    'NoColor',{
    token.NUMBER     : Colors.NoColor,
    token.OP         : Colors.NoColor,
    token.STRING     : Colors.NoColor,
    tokenize.COMMENT : Colors.NoColor,
    token.NAME       : Colors.NoColor,
    token.ERRORTOKEN : Colors.NoColor,

    _KEYWORD         : Colors.NoColor,
    _TEXT            : Colors.NoColor,

    'normal'         : Colors.NoColor  # color off (usu. Colors.Normal)
    }  )

LinuxColors = ColorScheme(
    'Linux',{
    token.NUMBER     : Colors.LightCyan,
    token.OP         : Colors.Yellow,
    token.STRING     : Colors.LightBlue,
    tokenize.COMMENT : Colors.LightRed,
    token.NAME       : Colors.White,
    token.ERRORTOKEN : Colors.Red,

    _KEYWORD         : Colors.LightGreen,
    _TEXT            : Colors.Yellow,

    'normal'         : Colors.Normal  # color off (usu. Colors.Normal)
    } )

LightBGColors = ColorScheme(
    'LightBG',{
    token.NUMBER     : Colors.Cyan,
    token.OP         : Colors.Blue,
    token.STRING     : Colors.Blue,
    tokenize.COMMENT : Colors.Red,
    token.NAME       : Colors.Black,
    token.ERRORTOKEN : Colors.Red,

    _KEYWORD         : Colors.Green,
    _TEXT            : Colors.Blue,

    'normal'         : Colors.Normal  # color off (usu. Colors.Normal)
    }  )

# Build table of color schemes (needed by the parser)
ANSICodeColors = ColorSchemeTable([NoColor,LinuxColors,LightBGColors], _scheme_default)

class Parser:
    """ Format colored Python source.
    """

    def __init__(self, color_table=None,out = sys.stdout):
        """ Create a parser with a specified color table and output channel.

        Call format() to process code.
        """
        self.color_table = color_table and color_table or ANSICodeColors
        self.out = out

    def format(self, raw, out = None, scheme = ''):
        return self.format2(raw, out, scheme)[0]

    def format2(self, raw, out = None, scheme = ''):
        """ Parse and send the colored source.

        If out and scheme are not specified, the defaults (given to
        constructor) are used.

        out should be a file-type object. Optionally, out can be given as the
        string 'str' and the parser will automatically return the output in a
        string."""
        
        string_output = 0
        if out == 'str' or self.out == 'str' or \
           isinstance(self.out,cStringIO.OutputType):
            # XXX - I don't really like this state handling logic, but at this
            # point I don't want to make major changes, so adding the
            # isinstance() check is the simplest I can do to ensure correct
            # behavior.
            out_old = self.out
            self.out = cStringIO.StringIO()
            string_output = 1
        elif out is not None:
            self.out = out

        # Fast return of the unmodified input for NoColor scheme
        if scheme == 'NoColor':
            error = False
            self.out.write(raw)
            if string_output:
                return raw,error
            else:
                return None,error
        
        # local shorthands
        colors = self.color_table[scheme].colors
        self.colors = colors # put in object so __call__ sees it

        # Remove trailing whitespace and normalize tabs
        self.raw = raw.expandtabs().rstrip()
        
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        raw_find = self.raw.find
        lines_append = self.lines.append
        while 1:
            pos = raw_find('\n', pos) + 1
            if not pos: break
            lines_append(pos)
        lines_append(len(self.raw))

        # parse the source and write it
        self.pos = 0
        text = cStringIO.StringIO(self.raw)

        error = False
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write("%s\n\n*** ERROR: %s%s%s\n" %
                           (colors[token.ERRORTOKEN],
                            msg, self.raw[self.lines[line]:],
                            colors['normal'])
                           )
            error = True
        self.out.write(colors['normal']+'\n')
        if string_output:
            output = self.out.getvalue()
            self.out = out_old
            return (output, error)
        return (None, error)

    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler, with syntax highlighting."""

        # local shorthands
        colors = self.colors
        owrite = self.out.write

        # line separator, so this works across platforms
        linesep = os.linesep

        # calculate new positions
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            owrite(linesep)
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            owrite(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a color group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = _KEYWORD
        color = colors.get(toktype, colors[_TEXT])

        #print '<%s>' % toktext,    # dbg

        # Triple quoted strings must be handled carefully so that backtracking
        # in pagers works correctly. We need color terminators on _each_ line.
        if linesep in toktext:
            toktext = toktext.replace(linesep, '%s%s%s' %
                                      (colors['normal'],linesep,color))

        # send text
        owrite('%s%s%s' % (color,toktext,colors['normal']))
            
def main(argv=None):
    """Run as a command-line script: colorize a python file or stdin using ANSI
    color escapes and print to stdout.

    Inputs:

      - argv(None): a list of strings like sys.argv[1:] giving the command-line
        arguments. If None, use sys.argv[1:].
    """

    usage_msg = """%prog [options] [filename]

Colorize a python file or stdin using ANSI color escapes and print to stdout.
If no filename is given, or if filename is -, read standard input."""

    parser = optparse.OptionParser(usage=usage_msg)
    newopt = parser.add_option
    newopt('-s','--scheme',metavar='NAME',dest='scheme_name',action='store',
           choices=['Linux','LightBG','NoColor'],default=_scheme_default,
           help="give the color scheme to use. Currently only 'Linux'\
 (default) and 'LightBG' and 'NoColor' are implemented (give without\
 quotes)")

    opts,args = parser.parse_args(argv)

    if len(args) > 1:
        parser.error("you must give at most one filename.")

    if len(args) == 0:
        fname = '-' # no filename given; setup to read from stdin
    else:
        fname = args[0]

    if fname == '-':
        stream = sys.stdin
    else:
        stream = file(fname)

    parser = Parser()

    # we need nested try blocks because pre-2.5 python doesn't support unified
    # try-except-finally
    try:
        try:
            # write colorized version to stdout
            parser.format(stream.read(),scheme=opts.scheme_name)
        except IOError,msg:
            # if user reads through a pager and quits, don't print traceback
            if msg.args != (32,'Broken pipe'):
                raise
    finally:
        if stream is not sys.stdin:
            stream.close() # in case a non-handled exception happened above

if __name__ == "__main__":
    main()

