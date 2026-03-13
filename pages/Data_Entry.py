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
    defaults = {
        "energy_kwh": 100000.0,
        "energy_cost_per_kwh": 0.12,
        "water_m3": 5000.0,
        "water_cost_per_m3": 2.50,
        "waste_tons": 50.0,
        "waste_cost_per_ton": 75.0,
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
                step=1000.0
            )
            energy_price = st.number_input(
                "Energy Cost (per kWh)", 
                value=float(st.session_state["energy_cost_per_kwh"]), 
                format="%.4f"
            )

            st.markdown("### 💧 Water Management")
            water = st.number_input(
                "Annual Water Usage (m³)", 
                value=float(st.session_state["water_m3"]), 
                step=100.0
            )
            water_price = st.number_input(
                "Water Cost (per m³)", 
                value=float(st.session_state["water_cost_per_m3"]), 
                format="%.2f"
            )

        with col2:
            st.markdown("### ♻️ Waste & Disposal")
            waste = st.number_input(
                "Annual Waste Generated (Tons)", 
                value=float(st.session_state["waste_tons"]), 
                step=1.0
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
            st.session_state["energy_kwh"] = energy
            st.session_state["energy_cost_per_kwh"] = energy_price
            st.session_state["water_m3"] = water
            st.session_state["water_cost_per_m3"] = water_price
            st.session_state["waste_tons"] = waste
            st.session_state["waste_cost_per_ton"] = waste_price
            st.success("✅ Baseline data updated successfully!")

if __name__ == "__main__":
    main()