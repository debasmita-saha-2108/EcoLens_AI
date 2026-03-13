import numpy as np

def calculate_carbon_emissions(energy_kwh, water_liters, waste_kg):
    # Emission factors (standard global averages)
    ENERGY_FACTOR = 0.475   # kg CO2 per kWh
    WATER_FACTOR = 0.0003   # kg CO2 per liter
    WASTE_FACTOR = 1.9      # kg CO2 per kg waste

    energy_emissions = energy_kwh * ENERGY_FACTOR
    water_emissions = water_liters * WATER_FACTOR
    waste_emissions = waste_kg * WASTE_FACTOR

    total = energy_emissions + water_emissions + waste_emissions

    return {
        "energy": round(energy_emissions, 2),
        "water": round(water_emissions, 2),
        "waste": round(waste_emissions, 2),
        "total": round(total, 2)
    }

def calculate_esg_score(environmental, social, governance):
    # Weighted average (40% Env, 30% Soc, 30% Gov)
    score = (environmental * 0.4) + (social * 0.3) + (governance * 0.3)
    return round(score, 2)

def generate_esg_breakdown(environmental, social, governance):
    return {
        "Environmental": environmental,
        "Social": social,
        "Governance": governance
    }