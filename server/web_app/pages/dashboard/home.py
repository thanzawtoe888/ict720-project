import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

def home(api_url):
    # Remove user_id from the API URL
    response = requests.get(f"{api_url}/get_data/user/{st.session_state['user_id']}")
    if response.status_code == 200:
        data = response.json()["data"]
        
        if data:
            # Convert JSON to DataFrame
            df = pd.DataFrame(data)

            # Remove the 'user_id' column
            df.drop(columns=['user_id'], inplace=True, errors='ignore')
            # Convert timestamp to datetime format
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
            
            # Display DataFrame
            st.write("### User Data")
            st.dataframe(df)

            # Plot BPM values if available
            if "bpm" in df.columns:
                code = '''# Plot BPM values if available
st.write("### BPM Over Time")
plt.figure(figsize=(10, 4))
plt.plot(df["timestamp"], df["bpm"], marker="o", linestyle="-")
plt.xlabel("Timestamp")
plt.ylabel("BPM")
plt.title("BPM Trend")
plt.xticks(rotation=45)
st.pyplot(plt)'''
                st.code(code, language="python")  # Display code
                st.write("### BPM Over Time")
                plt.figure(figsize=(10, 4))
                plt.plot(df["timestamp"], df["bpm"], marker="o", linestyle="-")
                plt.xlabel("Timestamp")
                plt.ylabel("BPM")
                plt.title("BPM Trend")
                plt.xticks(rotation=45)
                st.pyplot(plt)  # Plot BPM over time

            code = '''# Correlation Matrix Heatmap
st.write("### Correlation Matrix Heatmap")
correlation_matrix = df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
st.pyplot(plt)'''
            st.code(code, language="python")  # Display code for heatmap
            # Correlation Matrix Heatmap
            st.write("### Correlation Matrix Heatmap")
            correlation_matrix = df.corr()
            plt.figure(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title('Correlation Matrix Heatmap')
            st.pyplot(plt)  # Show heatmap

            code = '''# Pairplot - Visualizing pairwise relationships
st.write("### Pairplot")
sns.pairplot(df)
st.pyplot(plt)'''
            st.code(code, language="python")  # Display code for pairplot
            # Pairplot - Visualizing pairwise relationships
            st.write("### Pairplot")
            sns.pairplot(df)
            st.pyplot(plt)  # Show pairplot

        else:
            st.warning("No data found.")
    else:
        st.error("Failed to fetch data. Check API.")
