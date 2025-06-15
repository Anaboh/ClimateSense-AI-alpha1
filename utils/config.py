from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import hashlib
import os

def get_vector_store(report_path):
    # Create unique ID for report
    report_id = hashlib.md5(report_path.encode()).hexdigest()
    persist_path = f"data/chroma_db/{report_id}"
    
    # Create directory if not exists
    os.makedirs(persist_path, exist_ok=True)
    
    return Chroma(
        collection_name=f"ipcc_{report_id}",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        persist_directory=persist_path
    )
