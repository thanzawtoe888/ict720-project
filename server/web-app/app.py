import streamlit as st
import pandas as pd
import numpy as np
from components.sidebar import sidebar

# st.set_page_config(page_title="Streamlit Modular App")

pages = {
    "Application": [
        st.Page("./pages/dashboard/app.py", title="Dashboard"),
        st.Page("./pages/chatbot.py", title="Chatbot")
    ],
    "Account": [
        st.Page("./pages/create_account.py", title="Create your account"),
    ]
}
pg = st.navigation(pages)
pg.run()

sidebar()

# main page
# url = rest_station_api + station_id + '?mins=100000&rssi=-100'
# response = requests.get(url)
# station_data = response.json()
# df = pd.DataFrame(station_data)
# st.write(df)
