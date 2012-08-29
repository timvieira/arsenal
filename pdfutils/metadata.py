# pyPdf available at http://pybrary.net/pyPdf/
from pyPdf import PdfFileWriter, PdfFileReader

def metadata(filename):
    try:
        x = PdfFileReader(file(filename, 'rb'))
        return x.getDocumentInfo()
    except:
        return

def main():
    import sys
    for filename in (sys.argv[1:] or sys.stdin):
        print '--'
        filename = filename.strip()
        print filename
        try:
            m = metadata(filename)
            print m.title
            print m.author
            print
        except:
            print 'ERROR'


if __name__ == '__main__':
    main()
