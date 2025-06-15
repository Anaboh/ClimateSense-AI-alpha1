from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import hashlib

def get_vector_store(report_path):
    # Create unique ID for report
    report_id = hashlib.md5(report_path.encode()).hexdigest()
    
    return Chroma(
        collection_name=f"ipcc_{report_id}",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        persist_directory=f"data/chroma_db/{report_id}"
    )
