from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import hashlib
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import json

# Lightweight model for mobile
EMBEDDING_MODEL = "all-MiniLM-L6-v2" 

# Cache for vector stores
VECTOR_STORE_CACHE = {}

def get_vector_store(report_path):
    """Get vector store with mobile optimizations"""
    # Create unique ID for report
    report_id = hashlib.md5(report_path.encode()).hexdigest()
    
    # Use cached version if available
    if report_id in VECTOR_STORE_CACHE:
        return VECTOR_STORE_CACHE[report_id]
    
    persist_path = f"data/chroma_db/{report_id}"
    os.makedirs(persist_path, exist_ok=True)
    
    # Create vector store with smaller footprint
    vector_store = Chroma(
        collection_name=f"ipcc_{report_id}",
        embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL),
        persist_directory=persist_path
    )
    
    # Only process if empty
    if vector_store._collection.count() == 0 and os.path.exists(report_path):
        # Mobile-optimized processing
        loader = PyPDFLoader(report_path)
        docs = loader.load()
        
        # Smaller chunks for mobile
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Smaller for mobile
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(docs)
        
        # Add to vector store
        vector_store.add_documents(chunks)
    
    # Cache for future use
    VECTOR_STORE_CACHE[report_id] = vector_store
    return vector_store
