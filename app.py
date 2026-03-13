import streamlit as st

# 1. PAGE CONFIG (Must be first)
st.set_page_config(page_title="EcoLens AI", page_icon="🌿", layout="wide")

# 2. THE MASTER DATA BRIDGE
# We initialize these so the Dashboard and AI Report don't start with errors
if 'energy_kwh' not in st.session_state:
    st.session_state.energy_kwh = 1200
if 'water_liters' not in st.session_state:
    st.session_state.water_liters = 8000
if 'waste_kg' not in st.session_state:
    st.session_state.waste_kg = 320

# We create this specific dictionary because Iman's AI_Report.py needs it
st.session_state.carbon_data = {
    "energy": st.session_state.energy_kwh,
    "water": st.session_state.water_liters,
    "waste": st.session_state.waste_kg
}

# Iman's code also looks for 'initiatives', let's give it a default list
if 'initiatives' not in st.session_state:
    st.session_state.initiatives = ["Implementing smart sensors", "Optimizing supply chain"]

# 3. LANDING PAGE UI
st.title("🌿 EcoLens AI: Integrated ESG Platform")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Lead Architect Workspace")
    st.write("Welcome to the central hub. All team modules are now connected.")
    st.success("✅ System Status: All Shared States Initialized.")
    st.info("👈 Use the Sidebar to navigate to the Dashboard and AI Report.")

with col2:
    st.subheader("Team Integration Status")
    st.write(f"📊 **Dashboard:** Linked")
    st.write(f"🤖 **AI Engine:** Linked")
    st.write(f"📈 **ROI Sim:** Ready")