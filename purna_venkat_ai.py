import streamlit as st
from google import genai
import time
import random

# Set up the page FIRST (must be first Streamlit command)
st.set_page_config(
    page_title="Purna Venkat AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Then add your custom CSS
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
        background: linear-gradient(135deg, #0000FF 70%, #c3cfe2 12%);
    }
    
    .stChatInput {
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stChatMessage {
        border-radius: 15px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 16px !important;
    }
    
    [data-testid="stChatMessageContent"] {
        font-size: 1rem !important;
    }
    
    .user-message {
        background-color: var(--primary) !important;
        color: white !important;
        margin-left: 20% !important;
    }
    
    .assistant-message {
        background-color: white !important;
        margin-right: 20% !important;
        border: 1px solid #e0e0e0 !important;
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
    
    .logo {
        font-weight: 600;
        font-size: 1.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .logo-icon {
        font-size: 2rem;
    }
    
    .welcome-text {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize the client
client = genai.Client(api_key="AIzaSyCgryGGlwzincJg3x18S-JQfEz6t_Xmvv8")

# Header with logo
st.markdown("""
<div class="header">
    <div class="logo">
        <span class="logo-icon">✨</span>
        <span>Purna Venkat AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Namaste! I'm Purna Venkat AI, your intelligent assistant. How may I serve you today?",
        "animation": "fadeIn"
    }]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "animation" in message and message["animation"] == "typing":
            st.markdown("""
            <div class="typing-animation">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "animation": "fadeIn"
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add temporary typing indicator
    typing_message = {
        "role": "assistant",
        "content": "",
        "animation": "typing"
    }
    st.session_state.messages.append(typing_message)
    
    # Display typing animation
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-animation">
            <span></span>
            <span></span>
            <span></span>
        </div>
        """, unsafe_allow_html=True)
    
    # Simulate thinking time (minimum 0.5s to 1.5s)
    thinking_time = random.uniform(0.5, 1.5)
    time.sleep(thinking_time)
    
    # Get response from Gemini
    response = client.models.generate_content(
        model="gemini-1.5-pro-latest",
        contents=prompt
    )
    
    # Remove typing indicator
    st.session_state.messages.remove(typing_message)
    
    # Add assistant response to chat history
    assistant_message = {
        "role": "assistant",
        "content": response.text,
        "animation": "fadeIn"
    }
    st.session_state.messages.append(assistant_message)
    
    # Display assistant response with animation
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown(response.text)
    
    # Scroll to bottom
    st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
    </script>
    """, unsafe_allow_html=True)