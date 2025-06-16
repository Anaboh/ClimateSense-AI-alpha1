import streamlit as st
from agents.query_agent import get_climate_insights_streaming
from utils.reports import IPCC_REPORTS
import asyncio

# Perplexity-like UI
st.set_page_config(layout="wide", page_title="ClimateSense AI", page_icon="🌍")
st.title("🌍 ClimateSense AI")

with st.sidebar:
    st.header("IPCC Report Explorer")
    report_name = st.selectbox("Select Report", list(IPCC_REPORTS.keys()))
    st.divider()
    st.caption("Powered by Perplexity AI • IPCC Knowledge Base")
    st.caption("⚡ Optimized for policy makers")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.report = report_name

# Update report if changed
if st.session_state.report != report_name:
    st.session_state.messages = []
    st.session_state.report = report_name
    st.rerun()

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Ask about climate risks, policies, or insights..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display empty assistant message for streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        report_file = IPCC_REPORTS[report_name]
        
        # Stream response
        for chunk in get_climate_insights_streaming(prompt, report_file):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.caption(f"Source: {report_name}")
