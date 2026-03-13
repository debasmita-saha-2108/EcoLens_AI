import streamlit as st

st.set_page_config(
    page_title="EcoLens AI – ROI Simulator",
    page_icon="📈",
    layout="wide"
)

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

# ---------- ROI Calculations ----------
def calculate_energy_savings(baseline_kwh, reduction_pct, cost_per_kwh):
    reduction = baseline_kwh * (reduction_pct / 100)
    return reduction * cost_per_kwh

def calculate_water_savings(baseline_m3, reduction_pct, cost_per_m3):
    reduction = baseline_m3 * (reduction_pct / 100)
    return reduction * cost_per_m3

def calculate_waste_savings(baseline_tons, reduction_pct, cost_per_ton):
    reduction = baseline_tons * (reduction_pct / 100)
    return reduction * cost_per_ton

def calculate_payback(capex, annual_savings):
    if annual_savings <= 0:
        return float('inf')
    return capex / annual_savings

# ---------- MAIN APP ----------
def main():
    init_session()
    
    # Apply Green-Tech CSS
    st.markdown("""
    <style>
    body { background-color: #050908; }
    .stSlider > div > div > div[role="slider"] {
        background: linear-gradient(90deg, #145A32, #1D7A40);
        border: 1px solid #2ECC71;
    }
    .stButton > button {
        background: linear-gradient(90deg, #145A32, #0B3B24);
        color: #E9F5EC;
        border-radius: 0.5rem;
        border: 1px solid #1D7A40;
        font-weight: 500;
    }
    .stMetric > div > div > div {
        color: #CDE4D2;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    green_header(
        "🌱 ROI Simulator", 
        "Interactive calculator for sustainability investment payback periods"
    )

    st.markdown("**Enter your baseline data or use Data Entry page** | Real-time ROI updates")

    # ---------------- INPUTS ----------------
    st.markdown("---")
    
    # Baseline data (FIXED: Added float() wrapping to prevent MixedNumericTypesError)
    with st.expander("📊 Baseline Usage Data", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state["energy_kwh"] = st.number_input(
                "Annual Energy (kWh)", 
                value=float(st.session_state["energy_kwh"]), 
                min_value=0.0, step=10000.0
            )
        with col2:
            st.session_state["water_m3"] = st.number_input(
                "Annual Water (m³)", 
                value=float(st.session_state["water_m3"]), 
                min_value=0.0, step=500.0
            )
        with col3:
            st.session_state["waste_tons"] = st.number_input(
                "Annual Waste (tons)", 
                value=float(st.session_state["waste_tons"]), 
                min_value=0.0, step=5.0
            )

    # Investment sliders
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Investment Amounts")
        solar_capex = st.slider("Solar Panels ($)", 0, 500000, 150000, 10000)
        led_capex = st.slider("LED Lighting ($)", 0, 200000, 50000, 5000)
    
    with col2:
        st.markdown("### 📈 Efficiency Gains (%)")
        solar_pct = st.slider("Solar Reduction (%)", 0, 80, 40, 5)
        led_pct = st.slider("Lighting Reduction (%)", 0, 50, 25, 5)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        water_capex = st.slider("Water Systems ($)", 0, 150000, 40000, 5000)
        water_pct = st.slider("Water Reduction (%)", 0, 60, 20, 5)
    with col4:
        waste_capex = st.slider("Waste Systems ($)", 0, 100000, 30000, 5000)
        waste_pct = st.slider("Waste Reduction (%)", 0, 70, 30, 5)

    # ---------------- CALCULATIONS ----------------
    energy_solar = calculate_energy_savings(
        st.session_state["energy_kwh"], solar_pct, st.session_state["energy_cost_per_kwh"]
    )
    energy_led = calculate_energy_savings(
        st.session_state["energy_kwh"], led_pct, st.session_state["energy_cost_per_kwh"]
    )
    water_save = calculate_water_savings(
        st.session_state["water_m3"], water_pct, st.session_state["water_cost_per_m3"]
    )
    waste_save = calculate_waste_savings(
        st.session_state["waste_tons"], waste_pct, st.session_state["waste_cost_per_ton"]
    )

    total_capex = solar_capex + led_capex + water_capex + waste_capex
    total_savings = energy_solar + energy_led + water_save + waste_save
    payback_years = calculate_payback(total_capex, total_savings)

    # ---------------- RESULTS ----------------
    st.markdown("---")
    green_header("📊 Investment Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Investment", f"${total_capex:,.0f}")
    with col2:
        st.metric("Annual Savings", f"${total_savings:,.0f}")
    
    with col3:
        if payback_years < float('inf'):
            color = "normal" if payback_years <= 5 else "inverse"
            st.metric("Payback Period", f"{payback_years:.1f} years", delta_color=color)
        else:
            st.metric("Payback Period", "Never")

    # Savings Breakdown
    st.markdown("---")
    green_header("📈 Savings Breakdown")
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("**Energy Savings**")
        st.info(f"Solar: **${energy_solar:,.0f}/yr**")
        st.info(f"LED: **${energy_led:,.0f}/yr**")
    
    with b2:
        st.markdown("**Resource Savings**")
        st.success(f"Water: **${water_save:,.0f}/yr**")
        st.success(f"Waste: **${waste_save:,.0f}/yr**")

    # ROI Chart
    st.markdown("---")
    green_header("📉 Cumulative ROI Projection")
    
    if total_savings > 0:
        years = list(range(0, 11))
        # Cash flow: Starts at negative Capex, adds savings each year
        cash_flow = [(-total_capex) + (total_savings * i) for i in years]
        
        st.area_chart(cash_flow)
        st.caption("Chart shows cumulative cash flow over 10 years. Crossing the 0 line indicates the break-even point.")

if __name__ == "__main__":
    main()