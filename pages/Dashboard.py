import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.calculations import (
    calculate_carbon_emissions,
    calculate_esg_score,
    generate_esg_breakdown
)

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="EcoLens AI Dashboard",
    layout="wide",
    page_icon="🌱"
)

# -----------------------------------
# Green Tech Styling
# -----------------------------------
st.markdown(
    """
    <style>
    .metric-card {
        background-color:#0f2f1c;
        padding:20px;
        border-radius:10px;
        border: 1px solid #2e7d32;
    }
    .stMetric {
        background-color: rgba(46, 125, 50, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌱 EcoLens AI — ESG Dashboard")

# -----------------------------------
# Session State Defaults (Mock Data)
# -----------------------------------
if "energy_kwh" not in st.session_state:
    st.session_state.energy_kwh = 1200
if "water_liters" not in st.session_state:
    st.session_state.water_liters = 8000
if "waste_kg" not in st.session_state:
    st.session_state.waste_kg = 320
if "environmental_score" not in st.session_state:
    st.session_state.environmental_score = 75
if "social_score" not in st.session_state:
    st.session_state.social_score = 68
if "governance_score" not in st.session_state:
    st.session_state.governance_score = 80

# -----------------------------------
# Calculate Metrics & Success Celebrations
# -----------------------------------
emissions = calculate_carbon_emissions(
    st.session_state.energy_kwh,
    st.session_state.water_liters,
    st.session_state.waste_kg
)

esg_score = calculate_esg_score(
    st.session_state.environmental_score,
    st.session_state.social_score,
    st.session_state.governance_score
)

# --- SUCCESS CELEBRATION (Balloons & Toasts) ---
if esg_score >= 80:
    st.balloons()
    st.toast(f"🌟 Exceptional Performance! ESG Score: {esg_score}/100", icon="🍃")
elif esg_score >= 60:
    st.toast("✅ Solid ESG Performance. Keep improving!", icon="📈")

# --- Tree Offset Calculation ---
total_co2 = emissions['total']
trees_needed = total_co2 / 22

# -----------------------------------
# SIDEBAR ADVANCEMENTS
# -----------------------------------
st.sidebar.header("🌍 Sustainability Impact")
st.sidebar.metric(
    label="Forest Offset Required", 
    value=f"{int(trees_needed)} Trees",
    help="Number of mature trees needed to absorb your annual carbon footprint."
)

if trees_needed > 150:
    st.sidebar.warning("💡 High footprint. Switching to solar could save 40+ trees/year.")
else:
    st.sidebar.success("✅ Eco-Efficiency is high!")

st.sidebar.divider()

# --- Export Data as CSV ---
st.sidebar.subheader("📊 Export Reports")
report_data = {
    "Category": ["Energy", "Water", "Waste", "Environmental Score", "Social Score", "Governance Score"],
    "Value": [
        st.session_state.energy_kwh, 
        st.session_state.water_liters, 
        st.session_state.waste_kg,
        st.session_state.environmental_score,
        st.session_state.social_score,
        st.session_state.governance_score
    ]
}
df = pd.DataFrame(report_data)
csv = df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="📥 Download ESG Data (.csv)",
    data=csv,
    file_name='EcoLens_ESG_Report.csv',
    mime='text/csv',
)

# -----------------------------------
# KPI METRICS
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Carbon Emissions", f"{emissions['total']} kg CO2")

with col2:
    st.metric("Energy Emissions", f"{emissions['energy']} kg")

with col3:
    st.metric("Waste Emissions", f"{emissions['waste']} kg")

with col4:
    st.metric("ESG Score", f"{esg_score}/100", delta=f"{esg_score - 50}% vs Industry")

st.divider()

# -----------------------------------
# CHARTS
# -----------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Carbon Emission Breakdown")
    pie_data = {
        "Source": ["Energy", "Water", "Waste"],
        "Emissions": [emissions["energy"], emissions["water"], emissions["waste"]]
    }
    fig = px.pie(
        pie_data,
        names="Source",
        values="Emissions",
        hole=0.4, 
        color_discrete_sequence=["#1b5e20", "#2e7d32", "#66bb6a"]
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.subheader("ESG Performance Radar")
    esg_data = generate_esg_breakdown(
        st.session_state.environmental_score,
        st.session_state.social_score,
        st.session_state.governance_score
    )
    categories = list(esg_data.keys())
    values = list(esg_data.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], 
        theta=categories + [categories[0]],
        fill='toself',
        name='ESG Score',
        line=dict(color="#66bb6a", width=2),
        fillcolor="rgba(102, 187, 106, 0.3)"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#444")),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("EcoLens AI • ESG Intelligence Platform • Verified Analytics")