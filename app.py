import streamlit as st

st.set_page_config(
    page_title="Solar Energy Predictor",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Solar Energy Production Predictor")

st.write("""
Welcome to the Solar Energy Production Prediction App.
This app is successfully deployed on Streamlit Cloud.
""")

st.success("Deployment Successful!")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.write(f"Hello, {name}!")
