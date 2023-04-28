import streamlit as st

# Setting up page configurations
st.set_page_config(
    page_title="HR Prediction",
    page_icon="⚾",
    layout="wide")

# Setting up the page
weight = st.number_input('Weight')
height = st.number_input('Height')
G = st.number_input('G')
AB = st.number_input('AB')

# make a nice button that triggers creation of a new data-line in the format that the model expects and prediction
st.button('Predict! 🚀'):
