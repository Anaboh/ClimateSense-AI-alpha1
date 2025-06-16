from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from utils.config import get_vector_store
import os

def get_climate_insights_streaming(query, report_file):
    # Get precomputed vector store
    report_path = f"data/reports/{report_file}"
    vector_store = get_vector_store(report_path)
    
    # Initialize Perplexity with streaming
    llm = ChatOpenAI(
        openai_api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai",
        model="pplx-7b-online",  # Faster online model
        temperature=0.1,
        max_tokens=512,  # Shorter responses
        streaming=True   # Enable streaming
    )
    
    # Optimized prompt
    prompt_template = f"""
    [ROLE] Climate policy expert analyzing IPCC {report_file}
    [TASK] Provide key insights for policymakers in bullet points:
    - Focus on risks, mitigation strategies, quantified impacts
    - Include confidence levels (high/medium/low)
    - Keep responses under 300 words
    - Use emojis for emphasis
    
    [QUERY] {query}
    """
    
    # Create chain with streaming
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 2})  # Fewer chunks
    )
    
    # Stream response chunks
    for chunk in qa_chain.stream(prompt_template):
        if "text" in chunk:
            yield chunk["text"]
