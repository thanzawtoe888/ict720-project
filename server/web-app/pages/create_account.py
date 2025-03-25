import streamlit as st
import os
from components.form import registration_form

# Get environment variables
api_url = os.getenv('API_URL', None)

if api_url is None:
    raise ValueError('API URL are not set')

st.subheader('Register')
st.text('Register your accounts')
registration_form(api_url)
