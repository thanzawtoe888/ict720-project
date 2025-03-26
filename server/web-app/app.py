import streamlit as st
import pandas as pd
import numpy as np


# page settings
st.subheader('Fitness-Guys Application')
st.text('Taist ICT720-Group08')


# st.set_page_config(page_title="Streamlit Modular App")


pages = {
    "Application": [
        st.Page("./pages/dashboard/app.py", title="Dashboard"),
        st.Page("./pages/create_account.py", title="Create your account"),
    ],
    "Resources": [
        st.Page("./pages/learn.py", title="Learn about us")
    ]
}

pg = st.navigation(pages)
pg.run()

# main page
# url = rest_station_api + station_id + '?mins=100000&rssi=-100'
# response = requests.get(url)
# station_data = response.json()
# df = pd.DataFrame(station_data)
# st.write(df)
