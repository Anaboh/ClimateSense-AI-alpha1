from langchain_community.llms import Perplexity
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.config import get_vector_store

pplx = Perplexity(api_key=os.getenv("PERPLEXITY_API_KEY"))

def process_report(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    
    # Semantic chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)
    
    # Store in vector DB
    vector_store = get_vector_store()
    vector_store.add_texts(chunks)
    
    return f"Processed {len(chunks)} chunks from {file_path}"
