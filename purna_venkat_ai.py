import os
import streamlit as st
import google.generativeai as genai
import time
import random
import requests
from streamlit.components.v1 import html

# --- Page Configuration (MUST BE FIRST) ---
st.set_page_config(
    page_title="Purna Venkat AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AI Client Class (Handles API Fallbacks) ---
class AIClient:
    def __init__(self):
        self.paid_api_key = os.getenv('GEMINI_API_KEY')
        self.free_api_key = "AIzaSyCgryGGlwzincJg3x18S-JQfEz6t_Xmvv8"  # Replace with your free key
        self.free_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def generate_response(self, prompt):
        # Special response for creator questions
        creator_phrases = [
            "who made you", "who created you", 
            "who built you", "who developed you",
            "who is your creator", "who designed you"
        ]
        if any(phrase in prompt.lower() for phrase in creator_phrases):
            return "I was created by Purna Venkat sir, the brilliant visionary behind this AI system."
        
        # Try paid API first
        if self.paid_api_key:
            try:
                genai.configure(api_key=self.paid_api_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):
                    time.sleep(5)  # Respect rate limits
        
        # Fallback to free API
        try:
            params = {'key': self.free_api_key}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(self.free_api_url, json=payload, params=params)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            return "I'm currently at capacity. Please try again in a moment."

ai_client = AIClient()

# --- Premium CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #6C63FF;
        --secondary: #4D44DB;
        --accent: #FF6B6B;
        --light: #F8F9FA;
        --dark: #212529;
    }
    
    * {
        font-family: 'Montserrat', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f2 100%);
        background-attachment: fixed;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        animation: float 6s ease-in-out infinite;
    }
    
    .typing-animation {
        display: flex;
        gap: 5px;
        padding: 10px 15px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        width: fit-content;
    }
    
    .typing-dot {
        height: 10px;
        width: 10px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 50%;
        display: inline-block;
    }
    
    .typing-dot:nth-child(1) { animation: pulse 1.2s infinite 0s; }
    .typing-dot:nth-child(2) { animation: pulse 1.2s infinite 0.2s; }
    .typing-dot:nth-child(3) { animation: pulse 1.2s infinite 0.4s; }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    .message-entrance {
        animation: messageEntrance 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes messageEntrance {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Floating Particles Background ---
html("""
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
    "particles": {
        "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
        "color": {"value": "#6C63FF"},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.5, "random": true},
        "size": {"value": 3, "random": true},
        "line_linked": {"enable": true, "distance": 150, "color": "#6C63FF", "opacity": 0.4, "width": 1},
        "move": {"enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out", "bounce": false}
    }
});
</script>
""", height=0)

# --- App Header ---
st.markdown("""
<div class="header">
    <div style="font-weight: 700; font-size: 2rem; display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 2.5rem;">✨</span>
        <span style="text-shadow: 0 2px 4px rgba(0,0,0,0.1);">Purna Venkat AI</span>
    </div>
    <div style="font-weight: 300; font-size: 1rem; margin-top: 0.5rem;">
        World's Most Advanced AI Assistant
    </div>
</div>
""", unsafe_allow_html=True)

# --- Initialize Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Namaste! I'm Purna Venkat AI. How may I enlighten you today?",
        "animation": "message-entrance"
    }]

# --- Display Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="{message.get("animation", "")}">{message["content"]}</div>', 
                   unsafe_allow_html=True)

# --- Chat Input ---
if prompt := st.chat_input("Ask the world's smartest AI..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "animation": "message-entrance"
    })
    
    with st.chat_message("user"):
        st.markdown(f'<div class="message-entrance">{prompt}</div>', unsafe_allow_html=True)
    
    # Show typing indicator
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-animation">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Get AI response
    ai_response = ai_client.generate_response(prompt)
    
    # Remove typing indicator and show response
    typing_placeholder.empty()
    with st.chat_message("assistant"):
        st.markdown(f'<div class="message-entrance">{ai_response}</div>', unsafe_allow_html=True)
    
    # Add to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "animation": "message-entrance"
    })
    
    # Auto-scroll
    html("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
    </script>
    """, height=0)