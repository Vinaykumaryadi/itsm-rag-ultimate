from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def build_store(docs):
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    return Chroma.from_documents(docs, embeddings)