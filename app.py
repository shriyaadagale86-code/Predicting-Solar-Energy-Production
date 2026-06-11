import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Set up page configuration
st.set_page_config(
    page_title="Solar Production Optimizer",
    page_icon="☀️",
    layout="centered"
)

# Load the saved model and encoder
@st.cache_resource
def load_assets():
    with open('solar_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('solar_encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return model, encoder

try:
    loaded_model, loaded_encoder = load_assets()
except FileNotFoundError:
    st.error("Error: Model or Encoder file not found. Ensure 'solar_model.pkl' and 'solar_encoder.pkl' are in the same directory.")
    st.stop()

# Reconstructing known categories based on your notebook's top details
# (Streamlit needs lists to fill out the dropdown selection boxes)
utilities = ['Con Ed', 'National Grid', 'NYSEG', 'RG&E', 'Central Hudson', 'Orange & Rockland']
counties = ['Queens', 'Bronx', 'Kings', 'Lewis', 'Allegany', 'Tioga', 'Jefferson', 'Cortland', 'Nassau', 'Suffolk']
cities = ['Richmond Hill', 'Bronx', 'Brooklyn', 'Springfield Gardens', 'New York']
developers = ['Kamtech Solar Solutions', 'SUNCO', 'Vivint Solar', 'MOMENTUM SOLAR', 'Sunrun Inc', 'Solar City', 'Unknown']
metering_methods = ['NM', 'Net Metering', 'Remote Net Metering', 'Value Stack']

# UI Design
st.title("☀️ SOLAR DEPLOYMENT PROJECT OPTIMIZER")
st.markdown("Predict the **Estimated Annual PV Energy Production (kWh)** for upcoming solar project planning deployments.")
st.write("---")

st.header("Project Specifications")

# Column Layouts for inputs
col1, col2 = st.columns(2)

with col1:
    utility = st.selectbox("Utility Provider", options=sorted(utilities))
    county = st.selectbox("County Location", options=sorted(counties))
    city = st.text_input("City / Town", value="Richmond Hill")
    developer = st.selectbox("Project Developer", options=sorted(developers))
    metering = st.selectbox("Metering Method", options=sorted(metering_methods))

with col2:
    kwdc = st.number_input("Estimated PV System Size (kWdc)", min_value=0.01, max_value=50000.0, value=10.50, step=0.1)
    kwac = st.number_input("PV System Size (kWac)", min_value=0.01, max_value=40000.0, value=9.00, step=0.1)
    year = st.number_input("Interconnection Year", min_value=2020, max_value=2035, value=2026, step=1)
    month = st.slider("Interconnection Month", min_value=1, max_value=12, value=6)

st.write("---")

# Predict Button
if st.button("Optimize & Predict Production", type="primary"):
    # Format the input data to match the feature list order
    proposed_project = pd.DataFrame([{
        'Utility': utility,
        'County': county,
        'City/Town': city,
        'Developer': developer,
        'Metering Method': metering,
        'Estimated PV System Size (kWdc)': kwdc,
        'PV System Size (kWac)': kwac,
        'Interconnection Year': float(year),
        'Interconnection Month': float(month)
    }])
    
    cat_features = ['Utility', 'County', 'City/Town', 'Developer', 'Metering Method']
    
    try:
        # Transform categorical variables using the loaded OrdinalEncoder
        proposed_project[cat_features] = loaded_encoder.transform(proposed_project[cat_features])
        
        # Run prediction via Ridge Regression model
        prediction = loaded_model.predict(proposed_project)[0]
        final_prediction = max(0.0, prediction)
        
        # Display Results
        st.success("### Project Planning Analysis Finalized!")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Predicted Annual Production", value=f"{final_prediction:,.2f} kWh")
        with res_col2:
            st.metric(label="Configured Capacity", value=f"{kwdc} kWdc")
            
        st.info(f"**Target Location:** {city}, {county} County | **Developer:** {developer}")

    except Exception as e:
        st.error(f"An error occurred during prediction mapping: {e}")
