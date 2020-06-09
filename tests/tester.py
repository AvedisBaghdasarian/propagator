from src.pdfxtract import pdf_to_text
import numpy as np

import csv

numpdf = 10


pdflist = np.zeros(numpdf, dtype=object)
for i in np.arange(len(pdflist)):
        pdflist[i] = "data/local-directory/1001/1001." + str(i+1).zfill(4) + ".pdf"
print(pdflist)


text = pdf_to_text(pdflist)


with open('pdftexts.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(text)
