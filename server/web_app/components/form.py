import streamlit as st
import requests

def registration_form(api_url):
    # Streamlit form for user registration
    with st.form("registration_form"):
        st.subheader("Enter your details")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        email = st.text_input("Email", placeholder="Enter your email")
        first_name = st.text_input("First Name", placeholder="Enter your first name")
        last_name = st.text_input("Last Name", placeholder="Enter your last name")
        
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        nationality = st.text_input("Nationality", placeholder="Enter your nationality")
        
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
        
        phone_number = st.text_input("Phone Number", placeholder="Enter your phone number")
        company_name = st.text_input("Company Name", placeholder="Enter your company name")
        job = st.text_input("Job Title", placeholder="Enter your job title")
        
        submit_button = st.form_submit_button("Register")

    # Handle form submission
    if submit_button:
        user_data = {
            "username": username,
            "password": password,
            "email": email,
            "first-name": first_name,
            "last-name": last_name,
            "gender": gender,
            "nationality": nationality,
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "phone-number": phone_number,
            "company-name": company_name,
            "job": job
        }

        try:
            print(api_url + "/resgister" + "  \n", user_data)
            response = requests.post(api_url + "/resgister", json=user_data)
            result = response.json()

            if response.status_code == 201:
                st.success(f"✅ {result['message']}")
                st.info(f"User ID: {result['user_id']}")
            else:
                st.error(f"❌ Error: {result.get('error', 'Something went wrong')}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to connect to server: {e}")


def edit_profile_form(api_url):
    # Ensure the user is logged in
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("You need to log in first.")
        st.stop()

    token = st.session_state["token"]
    
    # Fetch current profile data
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/protected", headers=headers)

    if response.status_code != 200:
        st.error("Failed to fetch user details. Please log in again.")
        st.stop()

    # **Fetch current user profile**
    response = requests.get(f"{api_url}/get_profile", headers=headers)

    if response.status_code == 200:
        user_data = response.json()
    else:
        st.error("Failed to fetch profile data. Please log in again.")
        st.stop()

    # **Pre-fill form fields**
    email = st.text_input("Email", user_data.get("email", ""))
    phone = st.text_input("Phone Number", user_data.get("phone_number", ""))
    job = st.text_input("Job Title", user_data.get("job", ""))
    company = st.text_input("Company Name", user_data.get("company_name", ""))
    weight = st.text_input("Weight (kg)", str(user_data.get("weight", "")))
    height = st.text_input("Height (cm)", str(user_data.get("height", "")))

    if st.button("Save Changes"):
        update_data = {
            "email": email,
            "phone_number": phone,
            "job": job,
            "company_name": company,
            "weight": weight,
            "height": height,
        }

        update_data = {k: v for k, v in update_data.items() if v}  # Remove empty fields

        if not update_data:
            st.warning("No changes made.")
        else:
            response = requests.put(f"{api_url}/edit_profile", json=update_data, headers=headers)

            if response.status_code == 200:
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile.")
