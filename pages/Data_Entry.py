import streamlit as st

st.set_page_config(page_title="EcoLens AI – Data Entry", page_icon="📝", layout="wide")

# ---------- Green-Tech Theme ----------
def green_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="padding:0.5rem 0 0.2rem 0;">
            <h2 style="color:#CDE4D2; margin-bottom:0;">{title}</h2>
            <p style="color:#9AB8A0; margin-top:0.2rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Initialize session state ----------
def init_session():
    # These keys now match EXACTLY what Dashboard.py is looking for
    defaults = {
        "energy_kwh": 1200.0,
        "energy_cost_per_kwh": 0.12,
        "water_liters": 8000.0,
        "water_cost_per_m3": 2.50,
        "waste_kg": 320.0,
        "waste_cost_per_ton": 75.0,
        "environmental_score": 75,
        "social_score": 68,
        "governance_score": 80
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    init_session()
    
    green_header("📝 ESG Data Entry", "Update your baseline consumption metrics")

    st.info("Changes made here will automatically update the Dashboard and ROI Simulator.")

    with st.form("data_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚡ Energy & Utilities")
            energy = st.number_input(
                "Annual Energy Usage (kWh)", 
                value=float(st.session_state["energy_kwh"]), 
                step=100.0
            )
            energy_price = st.number_input(
                "Energy Cost (per kWh)", 
                value=float(st.session_state["energy_cost_per_kwh"]), 
                format="%.4f"
            )

            st.markdown("### 💧 Water Management")
            # We display m3 to the user, but store Liters for the Dashboard
            water_m3_input = st.number_input(
                "Annual Water Usage (m³)", 
                value=float(st.session_state["water_liters"] / 1000), 
                step=10.0
            )
            water_price = st.number_input(
                "Water Cost (per m³)", 
                value=float(st.session_state["water_cost_per_m3"]), 
                format="%.2f"
            )

        with col2:
            st.markdown("### ♻️ Waste & Disposal")
            # We display Tons to the user, but store kg for the Dashboard
            waste_tons_input = st.number_input(
                "Annual Waste Generated (Tons)", 
                value=float(st.session_state["waste_kg"] / 1000), 
                step=0.1
            )
            waste_price = st.number_input(
                "Waste Disposal Cost (per Ton)", 
                value=float(st.session_state["waste_cost_per_ton"]), 
                format="%.2f"
            )
            
            st.markdown("### 🏢 Operational Details")
            st.text_input("Facility Name", "Main Campus")
            st.date_input("Reporting Period Start")

        submit = st.form_submit_button("Save Baseline Data")

        if submit:
            # Update the core metrics the Dashboard uses
            st.session_state["energy_kwh"] = energy
            st.session_state["energy_cost_per_kwh"] = energy_price
            st.session_state["water_liters"] = water_m3_input * 1000 
            st.session_state["waste_kg"] = waste_tons_input * 1000
            st.session_state["water_cost_per_m3"] = water_price
            st.session_state["waste_cost_per_ton"] = waste_price
            
            # Logic: If they enter "Good" data, we reward them with a high ESG Score
            # This ensures the balloons trigger on the Dashboard
            if energy < 500 and waste_tons_input < 1:
                st.session_state["environmental_score"] = 95
                st.session_state["social_score"] = 90
                st.session_state["governance_score"] = 90
            else:
                # Default scores if data is average
                st.session_state["environmental_score"] = 75
                st.session_state["social_score"] = 68
                st.session_state["governance_score"] = 80
                
            st.success("✅ Baseline data updated! Head to the Dashboard for your celebration.")

if __name__ == "__main__":
    main()