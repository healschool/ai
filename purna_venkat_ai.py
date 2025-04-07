import os
import streamlit as st
import google.generativeai as genai  # Correct import
import time
import random

# --- Page Configuration (MUST BE FIRST) ---
st.set_page_config(
    page_title="Purna Venkat AI",
    page_icon="😂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Gemini Client ---

genai.configure(api_key=os.environ['GEMINI_API_KEY'])  # Standard environment variable name  # Make sure to set this in Streamlit Secrets

# --- Custom CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    :root {
        --primary: #6C63FF;
        --secondary: #4D44DB;
        --light: #F8F9FA;
        --dark: #212529;
    }
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg,  #b85042 50%, #e7e8d1 50%);
    }
    
    .typing-animation {
        display: inline-block;
    }
    
    .typing-animation span {
        height: 8px;
        width: 8px;
        background-color: var(--primary);
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        opacity: 0.4;
    }
    
    .typing-animation span:nth-child(1) {
        animation: pulse 1s infinite;
    }
    
    .typing-animation span:nth-child(2) {
        animation: pulse 1s infinite 0.2s;
    }
    
    .typing-animation span:nth-child(3) {
        animation: pulse 1s infinite 0.4s;
    }
    
    @keyframes pulse {
        0% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.4; transform: scale(1); }
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="header">
    <div style="font-weight: 600; font-size: 1.8rem; display: flex; align-items: center; gap: 10px;">
        <span>✨</span>
        <span>Purna Venkat AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Initialize Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I'm Purna Venkat. How may I help you today?"}
    ]

# --- Display Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show typing indicator
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-animation">
            <span></span>
            <span></span>
            <span></span>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate response
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        ai_response = response.text
    except Exception as e:
        ai_response = f"Sorry, I encountered an error: {str(e)}"
    
    # Remove typing indicator and show response
    typing_placeholder.empty()
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    
    # Add to conversation history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})