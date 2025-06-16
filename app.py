import streamlit as st
from agents.query_agent import get_smart_insights
from utils.reports import IPCC_REPORTS
from utils.error_handler import handle_errors
import time

# Mobile-responsive UI
st.set_page_config(
    layout="wide",
    page_title="ClimateSense AI",
    page_icon="🌍",
    initial_sidebar_state="collapsed"  # Better for mobile
)

# Mobile optimization CSS
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stTextInput>div>div>input { font-size: 16px !important; }
        .stButton>button { width: 100%; }
        .stSelectbox>div>div>div>div { font-size: 16px; }
        .stChatMessage { padding: 10px; }
    }
    .stSpinner>div>div { border-color: #4CAF50 transparent transparent transparent !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar for report selection
with st.sidebar:
    st.header("IPCC Report Explorer")
    report_name = st.selectbox("Select Report", list(IPCC_REPORTS.keys()))
    st.divider()
    st.caption("Powered by Perplexity AI • IPCC Knowledge Base")
    
    # Feedback mechanism
    with st.expander("💬 Help us improve"):
        feedback = st.text_area("Suggest improvement or report issue")
        if st.button("Submit Feedback"):
            from feedback_handler import save_feedback
            save_feedback(feedback)
            st.success("Thank you! We'll use this to improve.")

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
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        report_file = IPCC_REPORTS[report_name]
        
        try:
            # Get response with smart fallback
            for chunk in get_smart_insights(prompt, report_file):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            error_msg = handle_errors(e)
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.caption(f"Source: {report_name}")
