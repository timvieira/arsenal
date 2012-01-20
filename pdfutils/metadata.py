# pyPdf available at http://pybrary.net/pyPdf/
from pyPdf import PdfFileWriter, PdfFileReader
import sys


[filename] = sys.argv[1:]

x = PdfFileReader(file(filename, "rb"))

m = x.getDocumentInfo()

print '--'
print filename
print m.title
print m.author
print
