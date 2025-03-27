import streamlit as st
import requests
import os

st.markdown("""
    <style>

    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
            color:black;
        background: url('https://images.pexels.com/photos/2886937/pexels-photo-2886937.jpeg?auto=compress&cs=tinysrgb&w=1400');
        background-size: cover;
    } 

    .title-container {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color:black;
        border-radius:29px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }


    .chat-container {
        max-width: 700px;
        margin: auto;
        padding: 10px;
    }
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 18px;
        margin: 10px 10px;
        max-width: 80%;
        font-size: 16px;
        color: black;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    .user-bubble {
        text-align: right;
        margin-left: auto;
    }
    .assistant-bubble {
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown('<h1 class="title-container"> AI-Driven Farming Assistant </h1>', unsafe_allow_html=True)

if "message" not in st.session_state:
    st.session_state.message = []

st.write('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.message:
    role_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)
st.write('</div>', unsafe_allow_html=True)

if prompt := st.chat_input('ASK ANY QUERY FOR RELATED TO ORGANIC FARMING?'):
    st.session_state.message.append({'role': 'user', 'content': prompt})

    st.write('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDmv1XOROPjaFZukyX8K09_y35WvzpoAJE"
    
    data = {
        'contents': [{'parts': [{'text': prompt}]}]
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_json = response.json()
        response_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't generate a response.")

        st.session_state.message.append({'role': 'assistant', 'content': response_text})

        st.write('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble assistant-bubble">{response_text}</div>', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")