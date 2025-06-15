import streamlit as st
from agents.query_agent import get_climate_insights
from utils.reports import IPCC_REPORTS, get_report_filename

# Perplexity-like UI
st.set_page_config(layout="wide", page_title="ClimateSense AI", page_icon="🌍")
st.title("🌍 ClimateSense AI")

with st.sidebar:
    st.header("IPCC Report Explorer")
    report_name = st.selectbox("Select Report", list(IPCC_REPORTS.keys()))
    st.divider()
    st.caption("Powered by Perplexity AI • IPCC Knowledge Base")

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
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("Ask about climate risks, policies, or insights..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner(f"Analyzing {report_name}..."):
        try:
            report_file = get_report_filename(report_name)
            response = get_climate_insights(prompt, report_file)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)
            st.caption(f"Source: {report_name}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
