from langchain.chains import RetrievalQA
# REPLACE THIS:
# from langchain_openai import ChatOpenAI
# WITH THIS:
from langchain_community.chat_models import ChatOpenAI
from utils.config import get_vector_store
import os

def get_climate_insights(query, report_file):
    # Get report-specific vector store
    report_path = f"data/reports/{report_file}"
    vector_store = get_vector_store(report_path)
    
    # Initialize Perplexity via OpenAI SDK
    llm = ChatOpenAI(
        openai_api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai",
        model="pplx-7b-chat",
        temperature=0.1,
        max_tokens=1024
    )
    
    # Policy-focused prompt template
    prompt_template = f"""
    As a climate policy expert analyzing IPCC reports:
    - Provide actionable insights for policymakers
    - Highlight key risks and mitigation strategies
    - Quantify impacts where possible
    - Cite confidence levels (e.g., 'high confidence')
    - Format in bullet points with emojis
    - Reference specific report sections when possible
    
    Report: {report_file}
    Query: {query}
    """
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 4})
    )
    
    return qa_chain.run(prompt_template)
