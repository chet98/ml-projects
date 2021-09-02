import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
import nltk
nltk.download('punkt')
stemmer = PorterStemmer()
def tokenize (sentence):
     return nltk.word_tokenize(sentence)#return nltk.word_tokenize(sentence)

def stem (word):
    return stemmer.stem(word.lower())

def bag_of_words (tokenized_sentence, all_words):
    tokenized_sentence= [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag

# The main function of this code is to create the three functions, tokenize,stem, and bag_of_words according to the chatbot
# pipeline structure which can be used in  the further code