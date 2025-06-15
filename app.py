import streamlit as st
from agents.query_agent import get_climate_insights

# Perplexity-like UI
st.set_page_config(layout="wide")
st.title("🌍 ClimateSense AI")

with st.sidebar:
    st.header("IPCC Report Explorer")
    report = st.selectbox("Select Report", ["AR6 Synthesis Report", "Ocean & Cryosphere", "Global Warming 1.5°C"])
    st.divider()
    st.caption("Powered by Perplexity AI • IPCC Knowledge Base")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask about climate risks or policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Analyzing IPCC data..."):
        response = get_climate_insights(prompt, report)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    st.caption("Sources: IPCC AR6 Chapter 3 • Page 42-45")
