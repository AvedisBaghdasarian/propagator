"""
adapted from https://gist.github.com/jmcarp/7105045#file-pdfxtract-py
"""
"""
Extract PDF text using PDFMiner. Adapted from
http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import boto3
import tempfile

from io import StringIO

import json


def pdf_to_text(pdfnames):

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


        s3 = boto3.resource('s3')
        with tempfile.TemporaryFile() as f:
            s3.meta.client.download_fileobj('testpdflake', '1001/1001.0008.pdf', f)
            f.seek(0)
            print('hi', f)


            # Extract text
            fp = f
            for page in PDFPage.get_pages(fp):
                print('hi')
                interpreter.process_page(page)
            fp.close()


            # Get text from StringIO
            newtext = sio.getvalue()
            for word in dictionary:
                newtext = newtext.replace(word[0], word[1])

            text.append(newtext)
        print("hi" ,text)


    # Cleanup
    device.close()
    sio.close()


    return text
