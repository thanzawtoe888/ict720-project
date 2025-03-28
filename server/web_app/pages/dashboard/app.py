import streamlit as st
import requests
import os
from components.form import edit_profile_form
# Get environment variables
api_url = os.getenv('API_URL', None)

if api_url is None:
    raise ValueError('API URL are not set')

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

def logout():
    """Logout function"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

# If not authenticated, show login page
if not st.session_state["authenticated"]:
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        response = requests.post(f"{api_url}/login", json={"username": username, "password": password})

        # Parse JSON response
        data = response.json()  # Converts response to a Python dictionary

        # Access token and message
        token = data.get("token")  # Use .get() to avoid KeyError
        message = data.get("message")

        if response.status_code == 200:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["token"] = token
            st.success(message)
            st.rerun()  # Reload the page after login
        else:
            st.error("Invalid credentials")

# If authenticated, show dashboard
else:

    # Define the pages
    # st.sidebar.page_link("home", label="Home", icon="🏠")
    # st.sidebar.page_link("profile", label="Profile", icon="📄")

    # **Logout Button (At the Bottom)**
    if st.sidebar.button("🚪 Logout", key="logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["token"] = None
        st.success("Logged out successfully!")

    home, profile = st.tabs(["🏠 Home", "📄 Profile"])

    with home:
        st.header("A cat")
    with profile:
        st.write("Profile man.")
        edit_profile_form(api_url)