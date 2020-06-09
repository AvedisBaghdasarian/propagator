import PyPDF2 as pdf
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


#referenced https://medium.com/better-programming/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
def transcribe(filename):
    pdfobj = open(filename, "rb")
    pdfReader = pdf.PdfFileReader(pdfobj)

    num_pages = pdfReader.numPages
    count = 0
    text = ""

    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    if text != "":
        text = text

    else:
        text = textract.process(fileurl, method='tesseract', language='eng')
    return text

#referecned https://medium.com/better-programming/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
def tokenizetext(text):
    tokens = word_tokenize(text)
    keywords = [word for word in tokens]

    return keywords
