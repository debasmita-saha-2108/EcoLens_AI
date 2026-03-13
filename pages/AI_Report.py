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
        color: #333;
    }
    .stButton>button {
        background-color: #1b5e20;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .phase-card {
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 AI Strategy Report")
st.write("Instant ESG insights powered by Groq LPU technology.")

# --- ADVANCED LOGIC: Fetch Data from Session State ---
# We check for energy_kwh etc. which we defined in Dashboard
if 'energy_kwh' not in st.session_state:
    st.error("📥 Data Missing: Please visit the Dashboard or Data Entry first to initialize metrics.")
else:
    # Calculate Tree Offset for the AI Context
    # Using a simple logic here to match the Dashboard
    total_energy_emissions = st.session_state.energy_kwh * 0.5  # Typical factor
    total_waste_emissions = st.session_state.waste_kg * 0.1
    total_co2 = total_energy_emissions + total_waste_emissions
    trees_needed = int(total_co2 / 22)

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("🚀 Generate High-Speed AI Analysis"):
            with st.spinner("Analyzing metrics with Groq..."):
                # Pass data to the AI
                report_text = get_esg_analysis(
                    st.session_state.energy_kwh, 
                    st.session_state.waste_kg
                )
                
                st.markdown("### Strategic Overview")
                st.markdown(f'<div class="report-card">{report_text}</div>', unsafe_allow_html=True)
                
                # Advancement: Download AI Report as Text
                st.download_button(
                    label="📄 Download AI Summary",
                    data=report_text,
                    file_name="EcoLens_AI_Analysis.txt",
                    mime="text/plain"
                )

    with col2:
        st.markdown("### 🚀 Execution Roadmap")
        
        # Phase 1
        st.markdown(
            f"""<div class="phase-card" style="background-color: #2e7d32;">
            <strong>Phase 1: Reduction</strong><br>
            Targeting {int(total_co2 * 0.2)}kg reduction via HVAC optimization.
            </div>""", unsafe_allow_html=True)
        
        # Phase 2
        st.markdown(
            f"""<div class="phase-card" style="background-color: #388e3c;">
            <strong>Phase 2: Transition</strong><br>
            Offsetting {int(trees_needed * 0.4)} trees by switching to Solar.
            </div>""", unsafe_allow_html=True)
        
        # Phase 3
        st.markdown(
            f"""<div class="phase-card" style="background-color: #4caf50;">
            <strong>Phase 3: Net Zero</strong><br>
            Final {int(trees_needed * 0.6)} trees to be offset via carbon credits.
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.metric("Total Biotic Offset Required", f"{trees_needed} Trees")

st.divider()
st.caption("EcoLens AI • Powered by Groq LPU • ESG Intelligence")