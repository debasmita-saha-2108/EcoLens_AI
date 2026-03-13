import streamlit as st
from utils.ai_engine import get_esg_analysis

st.set_page_config(page_title="EcoLens AI | Report", page_icon="🌿", layout="wide")

# Dark Green Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8faf8; }
    .report-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #1b5e20;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #1b5e20;
        color: white;
        width: 100%;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 AI Strategy Report")
st.write("Instant ESG insights powered by Groq LPU technology.")

# Data Validation
if 'carbon_data' not in st.session_state or 'initiatives' not in st.session_state:
    st.error("📥 Data Missing: Please complete the 'Data Entry' section first.")
else:
    if st.button("🚀 Generate High-Speed Report"):
        with st.spinner("Analyzing metrics with Groq..."):
            # Call our updated ai_engine
            report_text = get_esg_analysis(
                st.session_state.carbon_data, 
                st.session_state.initiatives
            )
            
            st.markdown("### Strategic Overview")
            st.markdown(f'<div class="report-card">{report_text}</div>', unsafe_allow_html=True)
            
            st.success("Analysis complete. Use the sidebar to navigate to ROI Simulation for financial forecasting.")