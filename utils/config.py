from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import hashlib
import os
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Cache for vector stores
VECTOR_STORE_CACHE = {}

def get_vector_store(report_path):
    # Create unique ID for report
    report_id = hashlib.md5(report_path.encode()).hexdigest()
    
    # Use cached version if available
    if report_id in VECTOR_STORE_CACHE:
        return VECTOR_STORE_CACHE[report_id]
    
    persist_path = f"data/chroma_db/{report_id}"
    os.makedirs(persist_path, exist_ok=True)
    
    # Create vector store
    vector_store = Chroma(
        collection_name=f"ipcc_{report_id}",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        persist_directory=persist_path
    )
    
    # Cache for future use
    VECTOR_STORE_CACHE[report_id] = vector_store
    return vector_store

async def precompute_vector_store(report_path):
    """Precompute embeddings for faster responses"""
    if not os.path.exists(report_path):
        return f"Report not found: {report_path}"
    
    vector_store = get_vector_store(report_path)
    
    # Skip if already processed
    if vector_store._collection.count() > 0:
        return f"Vector store already exists for {report_path}"
    
    # Load and process document
    loader = PyPDFLoader(report_path)
    docs = loader.load()
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    
    # Add to vector store asynchronously
    await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: vector_store.add_documents(chunks)
    )
    
    return f"Precomputed vectors for {report_path}: {len(chunks)} chunks"
