from langchain.chains import RetrievalQA
from langchain_community.llms import Perplexity
from utils.config import get_vector_store

def get_climate_insights(query, report):
    prompt_template = f"""
    As a climate policy expert analyzing the IPCC {report} report:
    - Provide actionable insights for policymakers
    - Highlight key risks and mitigation strategies
    - Quantify impacts where possible
    - Cite confidence levels (e.g., 'high confidence')
    - Format in bullet points with emojis
    
    Question: {query}
    """
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=Perplexity(api_key=os.getenv("PERPLEXITY_API_KEY")),
        chain_type="stuff",
        retriever=get_vector_store().as_retriever()
    )
    
    return qa_chain.run(prompt_template)
