from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def get_vector_store():
    return Chroma(
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        persist_directory="data/chroma_db"
    )
