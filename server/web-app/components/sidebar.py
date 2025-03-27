import streamlit as st
import os

def sidebar():
    with st.sidebar:
        st.markdown("# Fitness Guys (Group 8)\n TAIST ICT720 Software Design")
        st.markdown("# About")
        st.markdown(
            "This is a health monitoring application that tracks the status of gym trainers in real time."
            "The system utilizes heart rate and motion sensors (IMU) to detect abnormal changes in trainers physical health during workouts."
        )
        st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/thanzawtoe888/ict720-project.git)")
        st.markdown("---")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        ""