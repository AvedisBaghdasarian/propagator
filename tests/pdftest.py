import sys
sys.path.append('./')
import nltk
nltk.download('punkt')
from src.pdf_analysis_tools import transcribe, tokenizetext

print(tokenizetext(transcribe("data/local-directory/1001/1001.0001.pdf")))
