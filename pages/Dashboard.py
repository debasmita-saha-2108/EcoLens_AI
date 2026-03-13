# pages/1_Dashboard.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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
    layout="wide"
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
# Calculate Metrics
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
    st.metric("ESG Score", f"{esg_score}/100")

st.divider()

# -----------------------------------
# CHARTS
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Carbon Emission Breakdown
# -----------------------------------

with col1:

    st.subheader("Carbon Emission Breakdown")

    pie_data = {
        "Source": ["Energy", "Water", "Waste"],
        "Emissions": [
            emissions["energy"],
            emissions["water"],
            emissions["waste"]
        ]
    }

    fig = px.pie(
        pie_data,
        names="Source",
        values="Emissions",
        color_discrete_sequence=["#1b5e20", "#2e7d32", "#66bb6a"]
    )

    fig.update_layout(
        paper_bgcolor="#0e1117",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# ESG Radar Chart
# -----------------------------------

with col2:

    st.subheader("ESG Performance")

    esg_data = generate_esg_breakdown(
        st.session_state.environmental_score,
        st.session_state.social_score,
        st.session_state.governance_score
    )

    categories = list(esg_data.keys())
    values = list(esg_data.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='ESG Score',
        line=dict(color="#2e7d32")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        paper_bgcolor="#0e1117",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.caption("EcoLens AI • ESG Intelligence Platform")