import numpy as np
#import tensorflow_hub as hub
import tensorflow
from keras import backend as K
import openai
from sklearn.neighbors import NearestNeighbors

class SemanticSearch:
    def __init__(self):
        '''
            The encoder that will embed the texts
        '''
        #self.use = hub.load('https://www.tfhub.dev/google/universal-sentence-encoder/4')
        self.use = tensorflow.saved_model.load('semantic_search_model')
        self.fitted = False


    def _get_text_embedding(self, texts, batch=1000):
        '''
            Returns embeddings for the tokens using the 
            universal sentence encoder from tensorflow hub.
        '''
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i:(i+batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings

    def fit(self, data, batch=1000, n_neighbors=5):
        '''
            The chunks will be fit so that the chunks with most semantic 
            similarity with the question asked will be returned in sorted manner
        '''
        self.data= data
        self.embeddings = self._get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]
        
        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

class Model:
    def __init__(self,KEY,chunk_data, question):
        self.KEY = KEY
        self.chunk_data = chunk_data
        self.question = question
        self.recommender = SemanticSearch()
        

    def _fetch_ordered_chunks(self):
        self.recommender.fit(self.chunk_data)
        ordered_chunks = self.recommender(self.question)
        return ordered_chunks
        
    def _createQuestionPrompt(self, n):
        topn_chunks = self._fetch_ordered_chunks()[:n]
        prompt= ""
        prompt += 'search results:\n\n'
        for c in topn_chunks:
            prompt+=c+'\n\n'
        prompt += "Instructions: Compose a comprehensive reply to the query using the search results given."\
              "Cite each reference using [number] notation (every result has this number at the beginning)."\
              "Citation should be done at the end of each sentence. If the search results mention multiple subjects"\
              "with the same name, create separate answers for each. Only include information found in the results and"\
              "don't add any additional information. Make sure the answer is correct and don't output false content."\
              "If the text does not relate to the query, simply state 'Found Nothing'. Don't write 'Answer:'"\
              "Directly start the answer.\n"
        prompt+= f"Query : {self.question} \n\n"
        return prompt
    
    def generateAnswer(self,n=3,engine ='text-davinci-003' ):
        prompt= self._createQuestionPrompt(n)
        openai.api_key = self.KEY
        completions = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=256,
            n=1,
            temperature=0,
        )
        answer = completions.choices[0]['text']
        K.clear_session()
        return answer