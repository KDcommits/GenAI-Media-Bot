import fitz
import re

class Data:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path 
        self.start_page = 1
        self.end_page = None
        self.word_length = 150

    def _preprocess(self,text):
        '''
        preprocess chunks
        1. Replace new line character with whitespace.
        2. Replace redundant whitespace with a single whitespace
        '''
        text = text.replace('\n', ' ')
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'\\u[e-f][0-9a-z]{3}',' ', text)
        return text
    
    def _pdf_to_text(self):
        '''
            convert pdf to a list of words.
        '''
        doc = fitz.open(self.pdf_path)
        total_pages= doc.page_count

        if self.end_page is None:
            self.end_page = total_pages
        text_list=[]

        for i in range(self.start_page-1, self.end_page):
            text= doc.load_page(i).get_text('text')
            text= self._preprocess(text)
            text_list.append(text)
        doc.close()
        return text_list
    
    def text_to_chunk(self):
        ''''
            converts the text into smaller chunks of word_length
        '''
        word_length= self.word_length
        texts = self._pdf_to_text()
        tokens = [text.split(' ') for text in texts]
        chunks=[]
        for idx, words in enumerate(tokens):
            for i in range(0,len(words), word_length):
                chunk = words[i:i+word_length]
                if (i+word_length) > len(words) and (len(chunk) < word_length) and (len(tokens) != (idx+1)):
                    tokens[idx+1] = chunk + tokens[idx+1]
                    continue
                chunk = ' '.join(chunk).strip()
                chunk=  f'[{idx+self.start_page}]'+' '+'"'+chunk+'"'
                chunks.append(chunk)
        return chunks