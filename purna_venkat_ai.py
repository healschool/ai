import os
import time
import random
import streamlit as st
import google.generativeai as genai
from streamlit.components.v1 import html
import google.api_core.exceptions

# --- Page Configuration ---
st.set_page_config(
    page_title="Purna Venkat",
    page_icon="😜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load API Key ---
API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Montserrat', sans-serif;
        transition: all 0.3s ease;
    }

    .stApp {
        background: linear-gradient(135deg, #000000 50%, #808080 50%);
        background-attachment: fixed;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    .header {
        background: linear-gradient(135deg, #6C63FF 0%, #4D44DB 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
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
        background: linear-gradient(135deg, #6C63FF 0%, #FF6B6B 100%);
        border-radius: 50%;
    }

    .typing-dot:nth-child(1) { animation: pulse 1.2s infinite 0s; }
    .typing-dot:nth-child(2) { animation: pulse 1.2s infinite 0.2s; }
    .typing-dot:nth-child(3) { animation: pulse 1.2s infinite 0.4s; }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
    }

    .message-entrance {
        animation: messageEntrance 0.5s ease;
    }

    @keyframes messageEntrance {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Floating Background with Particles ---
particles_js = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
    particlesJS("particles-js", {
        "particles": {
            "number": { "value": 80, "density": { "enable": true, "value_area": 800 }},
            "color": { "value": "#6C63FF" },
            "shape": { "type": "circle" },
            "opacity": { "value": 0.5, "random": true },
            "size": { "value": 3, "random": true },
            "line_linked": { "enable": true, "distance": 150, "color": "#6C63FF", "opacity": 0.4, "width": 1 },
            "move": { "enable": true, "speed": 2, "random": true, "straight": false, "out_mode": "out" }
        },
        "interactivity": {
            "events": {
                "onhover": { "enable": true, "mode": "repulse" },
                "onclick": { "enable": true, "mode": "push" }
            }
        }
    });
});
</script>
<div id="particles-js"></div>
"""
html(particles_js, height=0)

# --- Header ---
st.markdown("""
<div class="header">
    <div style="font-size: 2.5rem;">😜 <strong>Purna Venkat</strong></div>
    <div style="font-weight: 300;">World's Most Advanced AI Assistant</div>
</div>
""", unsafe_allow_html=True)

# --- Init Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Namaste! Nenu Mee Purna Venkat. Meku Emina Kavali Ante Chepandi. Nenu Meku Help Chesta?",
        "animation": "message-entrance"
    }]

# --- Display Previous Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "animation" in msg:
            st.markdown(f'<div class="{msg["animation"]}">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# --- Retry Logic ---
def generate_response_with_retries(model, prompt, max_retries=5):
    backoff = 1
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except google.api_core.exceptions.ResourceExhausted:
            wait_time = backoff + random.uniform(0, 1)
            st.warning(f"⚠️ Rate limit hit. Retrying in {wait_time:.1f} seconds...")
            time.sleep(wait_time)
            backoff *= 2
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    return "⚠️ Still hitting limits. Please try again tomorrow."

# --- Chat Input ---
if prompt := st.chat_input("Me Burralo Amina Questions Unte Ikkada Pettandi..."):
    st.session_state.messages.append({
        "role": "user", "content": prompt, "animation": "message-entrance"
    })
    with st.chat_message("user"):
        st.markdown(f'<div class="message-entrance">{prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        typing = st.empty()
        typing.markdown("""
        <div class="typing-animation">
            <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
        </div>
        """, unsafe_allow_html=True)

    lower_prompt = prompt.lower()
    creator_phrases = ["who made you", "who created you", "who built you", "who is your creator"]
    
    if any(phrase in lower_prompt for phrase in creator_phrases):
        ai_response = "I was created by **Purna Venkat**, the mastermind behind this intelligent assistant 😎"
    else:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        ai_response = generate_response_with_retries(model, prompt)

    typing.empty()
    with st.chat_message("assistant"):
        st.markdown(f'<div class="message-entrance">{ai_response}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant", "content": ai_response, "animation": "message-entrance"
    })

    html("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
    </script>
    """, height=0)
