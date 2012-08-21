import os
import glob
from subprocess import Popen

## TODO:
##   there might be a better solution to this
class file_specifier(object):
    """ just give file_specifier the any path (absolute or relative) and let if figure out the rest. """
    def __init__(self, path):

        #assert os.path.exists(path), '%s does not exist.' % path
        self.isfile = os.path.isfile(path)
        self.isdir  = os.path.isdir(path)
        self.islink = os.path.islink(path)

        self.abspath = os.path.abspath(path)
        (self.dir, self.name) = os.path.split(self.abspath)
        (noext, self.ext) = os.path.splitext(self.name)
        self.abs_noext = os.path.join(self.dir, noext)
        self.noext = noext
        self.relpath = os.path.relpath(path)

    def __repr__(self):
        return 'file_specifier {\n%s\n}' % ('\n'.join(map('  %8s: %s'.__mod__, self.__dict__.iteritems())))


def pdftotext(pdf, output=None, verbose=False, usecached=True):
    """Wraps a system call to pdftotext. """
    if not output:
        output = '{pdf.abspath}.d/pdftotext.txt'.format(pdf=file_specifier(pdf))
    output = os.path.abspath(output)
    outdir = os.path.dirname(output)
    # check if output directory exists
    if outdir and not os.path.exists(os.path.dirname(output)):
        if verbose:
            print '[pdftotext] making directory "%s"' % outdir
        os.makedirs(outdir)
    if usecached and os.path.exists(output):
        if verbose:
            print '[pdftotext] "%s" cached.' % pdf
    else:
        if verbose:
            print '[pdftotext] processing "%s"' % pdf
        p = Popen(['pdftotext', pdf, output], stdout=None, stderr=None)     # TODO: error checking
        p.wait()
        if verbose:
            if p.returncode == 0:
                print '[pdftotext] successfully processed "%s".' % (pdf,)
                print '[pdftotext] wrote "%s".' % (output,)
            else:
                print '[pdftotext] "%s" exited with status %s' % (pdf, p.returncode)
    try:
        # return contents of output file
        with file(output, 'r') as f:
            return f.read()
    except IOError:
        return ''


## TODO:
##   (!) make this a fsutil
##   take a list of files and globs
##   recursive option
##   timeout option
##   maybe a hook for pre/post-processing, useful for logging and zipping
##   check for success / failure
def pdf2image(input_files, outputdir_fmt='{f.abspath}.d', output_format='{f.noext}.page.%d.png',
              resolution=200, create_outputdir=True, testing=False, verbose=False):
    """
    Wraps a system call to ghostscript, which takes a pdf or postscript file
    and renders it to a series of images.

    Inputs:
        input_files:
            shell glob (e.g. '*.pdf', 'test.pdf') which specifiers the
            set of files to process.

        outputdir_fmt:
            e.g. '{f.name}.d', '{f.abspath}.d', 'papers/{f.name}.d';
            (see String formatting details)

        output_format:
            e.g. '{f.noext}.page.%d.png', '%d.png'; (see String formatting details)

        resolution:
            resolution to which ghostscript should ouput the image.

        create_outputdir:
            if this option is set to True and the output directory doesn't
            exist it will be created, it the option is set to False OSError
            will be raised.

        testing:
            setting this option to True will not execute the system call.

        verbose:
            prints information about what is going on.

    String formatting details:
    You can specify the various patterns for files using the str.format syntax,
    The variables you have access to in the formatting operations are:

        f:
            f is an instance of a file_specifier, which corresponds to a single
            file matching the input_files pattern.

            file_specifiers offers the following attributes: f.noext, f.name,
            f.abspath, f.ext, f.dir, f.relpath

        outputdir:
            outputdir_fmt after the missing slots have been filled in.
            e.g. if outputdir='{filename}.d' filename will be filled
            in with the appropriate string.

        resolution:
            resolution which ghostscript should render to
    """

    opts = '-dBATCH -dNOPAUSE -sDEVICE=png256'

    for f in map(file_specifier, glob.glob(input_files)):
        info = dict(f=f, opts=opts, resolution=resolution)
        outputdir = outputdir_fmt.format(**info)
        info['outputdir'] = outputdir

        if verbose:
            print 'processing:', f.abspath
            print '  * outputdir: ', outputdir

        if not os.path.exists(outputdir):
            if create_outputdir:
                if verbose:
                    print '  * created outputdir'
                os.makedirs(outputdir)
            else:
                raise OSError('Directory does not exists: %s' % outputdir)

        cmd = "gs -q -r{resolution} {opts} -sOutputFile=" + outputdir + "/" + output_format + ' "{f.abspath}"'
        cmd = cmd.format(**info)

        if verbose:
            print '  * System Call:'
            print '   ', cmd

        if not testing:
            os.system(cmd)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        pdf2image(sys.argv[1], outputdir_fmt='{f.noext}.d', verbose=True, testing=False)
    else:
        print 'usage: <file>'
