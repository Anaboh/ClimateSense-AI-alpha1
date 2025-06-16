from langchain_community.chat_models import ChatOpenAI
from utils.config import get_vector_store
from utils.error_handler import should_fallback
from langchain.prompts import PromptTemplate
import os
import requests
import time

def get_smart_insights(query, report_file, max_retries=2):
    # Try report-based response first
    report_path = f"data/reports/{report_file}"
    vector_store = get_vector_store(report_path)
    
    # Try local retrieval first
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    context_docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    # Smart prompt with fallback logic
    prompt_template = PromptTemplate.from_template(
        """
        [ROLE] Climate policy expert
        [TASK] Answer user question using IPCC report context when available
        [REPORT] {report_file}
        [CONTEXT] {context}
        [FALLBACK] If context is insufficient, use general knowledge but state it's not from the report
        [OUTPUT] Use bullet points with emojis, max 300 words
        
        [QUESTION] {query}
        """
    )
    
    # Initialize LLM with fast model
    llm = ChatOpenAI(
        openai_api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai",
        model="pplx-7b-online",
        temperature=0.1,
        max_tokens=400,
        streaming=True
    )
    
    # Format prompt
    prompt = prompt_template.format(
        report_file=report_file,
        context=context,
        query=query
    )
    
    # Retry logic with fallback detection
    for attempt in range(max_retries + 1):
        try:
            for chunk in llm.stream(prompt):
                yield chunk.content
            break  # Success, exit loop
        except (requests.exceptions.RequestException, Exception) as e:
            if attempt < max_retries and not should_fallback(e):
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                # Fallback to simpler response
                yield "⚠️ Our climate experts are busy. Here's a quick insight:\n\n"
                yield get_fallback_insight(query)
                break

def get_fallback_insight(query):
    """Generate insight without API when all else fails"""
    # Simple rule-based fallback
    climate_keywords = {
        "temperature": "Global temperatures are rising at unprecedented rates",
        "sea level": "Sea levels are rising due to thermal expansion and ice melt",
        "mitigation": "Key mitigation strategies include renewable energy and reforestation",
        "adaptation": "Adaptation measures include coastal protection and resilient agriculture"
    }
    
    for keyword, response in climate_keywords.items():
        if keyword in query.lower():
            return f"🌐 {response} (general knowledge)"
    
    return "🌐 Climate change requires urgent global action across all sectors (general knowledge)"
