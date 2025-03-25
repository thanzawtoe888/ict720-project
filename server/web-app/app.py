import streamlit as st
import pandas as pd
import numpy as np


# page settings
st.subheader('Fitness-Guys Application')
st.text('Taist ICT720-Group08')


# st.set_page_config(page_title="Streamlit Modular App")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Register"])
station_id = st.sidebar.selectbox('Station', ['esp32', 'ESP32'])


pages = {
    "Your account": [
        st.Page("./pages/create_account.py", title="Create your account"),
        st.Page("./pages/manage_account.py", title="Manage your account"),
    ]
    # ,
    # "Resources": [
    #     st.Page("learn.py", title="Learn about us"),
    #     st.Page("trial.py", title="Try it out"),
    # ],
}

pg = st.navigation(pages)
pg.run()

# main page
# url = rest_station_api + station_id + '?mins=100000&rssi=-100'
# response = requests.get(url)
# station_data = response.json()
# df = pd.DataFrame(station_data)
# st.write(df)
