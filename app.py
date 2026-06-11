import streamlit as st
import pandas as pd
import pickle

# Load model and encoder
with open("solar_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("solar_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

st.set_page_config(page_title="Solar Energy Predictor", page_icon="☀️")

st.title("☀️ Solar Energy Production Predictor")

# User Inputs
utility = st.text_input("Utility", "Con Ed")
county = st.text_input("County", "Queens")
city = st.text_input("City/Town", "Richmond Hill")
developer = st.text_input("Developer", "Kamtech Solar Solutions")
metering = st.text_input("Metering Method", "NM")

kwdc = st.number_input(
    "Estimated PV System Size (kWdc)",
    min_value=0.0,
    value=10.5
)

kwac = st.number_input(
    "PV System Size (kWac)",
    min_value=0.0,
    value=9.0
)

year = st.number_input(
    "Interconnection Year",
    min_value=2000,
    max_value=2100,
    value=2026
)

month = st.number_input(
    "Interconnection Month",
    min_value=1,
    max_value=12,
    value=6
)

if st.button("Predict Production"):

    data = pd.DataFrame([{
        "Utility": utility,
        "County": county,
        "City/Town": city,
        "Developer": developer,
        "Metering Method": metering,
        "Estimated PV System Size (kWdc)": kwdc,
        "PV System Size (kWac)": kwac,
        "Interconnection Year": year,
        "Interconnection Month": month
    }])

    cat_cols = [
        "Utility",
        "County",
        "City/Town",
        "Developer",
        "Metering Method"
    ]

    data[cat_cols] = encoder.transform(data[cat_cols])

    prediction = model.predict(data)[0]
    prediction = max(0, prediction)

    st.success(
        f"Predicted Annual PV Energy Production: {prediction:,.2f} kWh"
    )

    st.metric(
        "Annual Production (kWh)",
        f"{prediction:,.2f}"
    )
