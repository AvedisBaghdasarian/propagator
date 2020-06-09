
"""
adapted from https://gist.github.com/jmcarp/7105045#file-pdfxtract-py
"""
"""
Extract PDF text using PDFMiner. Adapted from
http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
"""
import time
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO

def pdf_to_text(pdfnames):
    t = time.time()
    text = []
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    dictionary = [["ﬀ" , "ff"],["ﬁ","fi"],["ﬂ", "fl"],['ﬃ', 'ffi'],['ﬄ', 'ffl'],['ﬅ', 'ft'],['ﬆ', 'st'], ['"', ''],["'",'' ] ]

    for pdfname in pdfnames:
        # Extract text
        print(pdfname)
        fp = open(pdfname, 'rb')
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()


        # Get text from StringIO
        newtext = sio.getvalue()
        for word in dictionary:
            newtext = newtext.replace(word[0], word[1])

        text.append(newtext)
        print(time.time()-t)

    # Cleanup
    device.close()
    sio.close()


    return text
