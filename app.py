import streamlit as st

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "United Arab Emirates": {
        "Transportation": 0.25,  # kgCO2/km
        "Electricity": 0.55,  # kgCO2/kWh
        "Diet": {
            "Plant-based": 0.5,  # kgCO2/meal
            "Mixed diet": 1.5,  # kgCO2/meal
            "Meat-heavy diet": 2.5  # kgCO2/meal
        },
        "Waste": 0.8  # kgCO2/kg
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Calculate your carbon footprint")

# Streamlit app code
st.title("Calculate your carbon footprint 🗺️🦶")

# User inputs
st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["United Arab Emirates"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Daily commute distance (in km)")
    use_slider_for_distance = st.checkbox("Use Slider", True)
    if use_slider_for_distance:
        distance = st.slider("Distance", 0.0, 100.0, key="distance_input")
    else:
        distance = st.text_input("Distance", "0.0")

    st.subheader("💡 Monthly electricity consumption (in kWh)")
    use_slider_for_electricity = st.checkbox("Use Slider", True)
    if use_slider_for_electricity:
        electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")
    else:
        electricity = st.text_input("Electricity", "0.0")

with col2:
    st.subheader("🗑️ Waste generated per week (in kg)")
    use_slider_for_waste = st.checkbox("Use Slider", True)
    if use_slider_for_waste:
        waste = st.slider("Waste", 0.0, 100.0, key="waste_input")
    else:
        waste = st.text_input("Waste", "0.0")

    st.subheader("🍽️ Number of meals per day")
    meals = st.number_input("Meals", 0, key="meals_input")

# Normalize inputs
if use_slider_for_distance:
    distance = distance * 365  # Convert daily distance to yearly
else:
    distance = float(distance)

if use_slider_for_electricity:
    electricity = electricity * 12  # Convert monthly electricity to yearly
else:
    electricity = float(electricity)

if meals > 0:
    meals = meals * 365  # Convert daily meals to yearly

if use_slider_for_waste:
    waste = waste * 52  # Convert weekly waste to yearly
else:
    waste = float(waste)

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
diet_type = st.radio("Select your diet type", ["Plant-based", "Mixed diet", "Meat-heavy diet"])
diet_emissions = EMISSION_FACTORS[country]["Diet"][diet_type] * meals
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):
    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet ({diet_type}): {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        avg_sequestration_per_tree = 0.022  # Average CO2 sequestration per tree in metric tonnes
        trees_required = round(total_emissions / avg_sequestration_per_tree, 2)
        st.warning(f"🌳 This is equivalent to the CO2 absorbed by approximately {trees_required} trees in a year")
