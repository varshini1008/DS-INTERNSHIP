import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

data=pd.read_csv(r"Final_dataset1.csv")


# Apply np.fromstring to convert string representations of arrays to NumPy arrays
data["Document_Vector"] = data["Document_Vector"].apply(lambda x : np.fromstring(x[1:-1], sep=' '))

# Print the values of the Document_Vector column after conversion


model=Word2Vec.load("word2vec_model.bin")


def document_vector(tokens, word2vec_model):
    document_vector = np.zeros(word2vec_model.vector_size)  # Initialize document vector
    count = 0  # Counter to keep track of valid word vectors
    for token in tokens:
        if token in word2vec_model.wv:
            document_vector += word2vec_model.wv[token]
            count += 1
    if count > 0:
        document_vector /= count  # Take the average of word vectors
    return document_vector

def calculate_similarity(query_vector, document_vectors):
    similarities = cosine_similarity([query_vector], document_vectors).flatten()
    return similarities

def find_similar_documents(query, data, model):
    query_vector = document_vector(query, model)
    document_vectors = np.array(data['Document_Vector'].tolist())
    similarities = calculate_similarity(query_vector, document_vectors)
    sorted_indices = np.argsort(similarities)[::-1]
    similar_documents = data.iloc[sorted_indices]
    return similar_documents

st.title("📽Movie Subtitle Search Engine")
st.subheader("🔎Search the related document")
q1=st.text_input("your text goes here... ")
if st.button("Search"):
    docs=find_similar_documents(q1,data,model)
    for i, (doc) in enumerate(docs["Series/Movie"].head(10), start=1):
        st.subheader(f"Document {i}")
        st.write(doc)
