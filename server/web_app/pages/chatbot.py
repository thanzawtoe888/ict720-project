import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import joblib


api_key = os.getenv("GOOGLE_API_KEY")

# Get environment variables
api_url = os.getenv('API_URL', None)

if api_url is None:
    raise ValueError('API URL are not set')

# Set up the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


asset_map = {
    'User-Demo 1': 1279,
    'User-Demo 2': 1292,
    'User-Demo 3': 1322
}

asset_id = st.sidebar.selectbox('Demo ID',['User-Demo 1', 'User-Demo 2', 'User-Demo 3'])

# Get the corresponding value for the selected asset
asset_value = asset_map[asset_id]
# Load the trained model
model = joblib.load("models/luca_prediction.pkl")
# Function to load data from a JSON file
def load_data_from_json(filename='data.json'):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)  # Load the JSON data into a Python object
    return data

# Function to find records by user_id
def find_by_user_id(data, user_id):
    results = []
    for record in data:
        if record.get("user_id") == user_id:
            results.append(record)
    return results

# Function to fetch user data
def fetch_asset_data():
    # Load data from JSON file
    data = load_data_from_json('json/users_demo.json')
    found_records = find_by_user_id(data,asset_value)
    # Print the results
    if found_records:
        for record in found_records:
            print(record)
    else:
        print(f"No records found for user_id: {asset_value}")
    return found_records

# Function to predict asset location based on BLE data
def make_prediction(context_json):
    try:
        # Convert JSON string to Python dictionary
        data = json.loads(context_json)

        # Extract relevant features
        features = [
            data.get("spo2", 0),          # Oxygen saturation level
            data.get("bpm", 0),           # Heart rate (beats per minute)
            data.get("excercise_mode", 0), # Exercise mode (1 = active, 0 = inactive)
            data.get("age", 0),           # Age of user
            data.get("weight_kg", 0),     # Weight in kg
            data.get("height_cm", 0)      # Height in cm
        ]

        # Convert to NumPy array (reshape for single input)
        X_input = np.array(features).reshape(1, -1)

        # Make prediction
        prediction = model.predict(X_input)

        return f"Predicted result: {prediction[0]}"

    except Exception as e:
        return f"Error in prediction: {str(e)}"

context_json = fetch_asset_data()

# df = pd.DataFrame()
# # Display DataFrame
# st.write("### User Data")
# st.dataframe(df)

# UI for API key
st.title('GenAI App')
# asset_id = st.sidebar.selectbox('Asset ID',['Asset-0', 'Asset-1', 'Asset-2', 'Asset-3'])
# asset_data = fetch_asset_data(asset_id)
# context_json = json.dumps(asset_data, indent=2)

# UI for chatbot
chat_ui, data_ui, predict_ui = st.tabs(["Chatbot", "Raw data", "Luca prediction"])

with chat_ui:
    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    user_input = st.chat_input("Question: ...")
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        # Construct prompt with context
        prompt = f'''
        Now, answer the following question based on the JSON data:
        {user_input}
        Do not give JSON data in the answer.
        {context_json}
        Here is the info about the A health-tracking application  with M5-Stick-C and MAX3010x technology.

        JSON data contains the following fields:
            "timestamp" is the time of observation
            "spo2" is the received signal strength indicator, bigger is closer to the station
            "bpm" BMI ->> four catagories : -Underweight = < 18.5 -Normal weight = 18.5 - 24.9 -Overweight = 25-29.9 -Obesity = BMI of 30 or greater
            "excercise_mode" there have only 1, and 2 value.
            "age"
            "gender"
            "weight_kg":
            "height_cm"
        '''

        # If the user asks for a prediction, apply the model
        if "predict" in user_input.lower():
            prediction_result = make_prediction(context_json)
            prompt += f"\nPrediction Result: {prediction_result}"

        # Generate response
        response = llm.invoke([HumanMessage(content=prompt)])
        st.session_state.messages.append(AIMessage(content=response.content))
        with st.chat_message("assistant"):
            st.write(response.content)

with data_ui:
    st.json(context_json)


with predict_ui:
    
    code = '''# Define features and target
    df = context_json
    x = df[['age', 'gender', 'weight_kg', 'height_cm', 'spo2', 'bpm']]
    y = df['excercise_mode']
    st.dataframe(x)
    '''
    st.code(code, language="python")

    code = '''# Split dataset
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Normalize numerical features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    '''
    st.code(code, language="python")
    
    code = '''import joblib
    # Train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model to a file
    joblib.dump(model, 'random_forest_model.pkl')
    '''
    st.code(code, language="python")

    code = '''# Predictions
    y_pred = model.predict(X_test)

    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    print(classification_report(y_test, y_pred))
    '''
    st.code(code, language="python")

