import os
import streamlit as st
import google.generativeai as genai
import time
import random
from streamlit.components.v1 import html

# --- Page Configuration ---
st.set_page_config(
    page_title="Purna Venkat",
    page_icon="😜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Gemini Client ---
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

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
        background: linear-gradient(135deg, #000000 50%, ##808080 50%);
        background-attachment: fixed;
    }
    
    /* Floating animation for header */
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
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        transform: rotate(30deg);
    }
    
    /* Advanced typing animation */
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
    
    .typing-dot:nth-child(1) {
        animation: pulse 1.2s infinite 0s;
    }
    
    .typing-dot:nth-child(2) {
        animation: pulse 1.2s infinite 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation: pulse 1.2s infinite 0.4s;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Message animations */
    .message-entrance {
        animation: messageEntrance 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes messageEntrance {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--primary), var(--secondary));
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Floating Particles Background ---
particles_js = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    particlesJS("particles-js", {
        "particles": {
            "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
            "color": {"value": "#6C63FF"},
            "shape": {"type": "circle"},
            "opacity": {"value": 0.5, "random": true},
            "size": {"value": 3, "random": true},
            "line_linked": {"enable": true, "distance": 150, "color": "#6C63FF", "opacity": 0.4, "width": 1},
            "move": {"enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out", "bounce": false}
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {"enable": true, "mode": "repulse"},
                "onclick": {"enable": true, "mode": "push"}
            }
        }
    });
});
</script>
<div id="particles-js"></div>
"""
html(particles_js, height=0)

# --- Premium App Header ---
st.markdown("""
<div class="header">
    <div style="font-weight: 700; font-size: 2rem; display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 2.5rem;">😜</span>
        <span style="text-shadow: 0 2px 4px rgba(0,0,0,0.1);">Purna Venkat</span>
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
        "content": "Namaste! Nenu Mee Purna Venkat,Meku Emina Kavali Ante Chepandi. Nenu Meku Help Chesta?",
        "animation": "message-entrance"
    }]

# --- Display Messages with Animations ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "animation" in message:
            st.markdown(f'<div class="{message["animation"]}">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# --- Premium Chat Input ---
if prompt := st.chat_input("Me Burralo Amina Questions Unte Ikkada Pettandi..."):
    # Add user message with animation
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "animation": "message-entrance"
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="message-entrance">{prompt}</div>', unsafe_allow_html=True)
    
    # Show premium typing indicator
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-animation">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if user is asking who created the AI
    if any(phrase in prompt.lower() for phrase in ["who made you", "who created you", "who built you", "who developed you",'what is your name']):
        ai_response = "I was created by Purna Venkat sir, the brilliant mind behind this advanced AI system."
    else:
        # Generate normal response
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt)
            ai_response = response.text
        except Exception as e:
            ai_response = f"Apologies, my quantum processors encountered a glitch: {str(e)}"
    
    # Remove typing indicator and show animated response
    typing_placeholder.empty()
    with st.chat_message("assistant"):
        st.markdown(f'<div class="message-entrance">{ai_response}</div>', unsafe_allow_html=True)
    
    # Add to conversation history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "animation": "message-entrance"
    })
    
    # Auto-scroll to bottom
    html("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
    </script>
    """, height=0)