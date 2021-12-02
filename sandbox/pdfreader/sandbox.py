from PyPDF2 import PdfFileReader

with open('Appendix_B.pdf', 'rb') as f:
    reader = PdfFileReader(f)
    contents = reader.getPage(1).extractText()
    print(contents)