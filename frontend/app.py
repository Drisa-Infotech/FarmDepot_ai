import streamlit as st
import requests
import os
from googletrans import Translator
from pydub import AudioSegment
from io import BytesIO

# Set page config
st.set_page_config(page_title="FarmDepot.ai", layout="wide")

# Initialize translator
translator = Translator()

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigate",
    [
        "Home",
        "Post Product (Voice)",
        "Register (Voice)",
        "Search Products",
        "Settings"
    ]
)

lang = st.sidebar.selectbox(
    "Choose Language",
    ["English", "Hausa", "Yoruba", "Igbo"]
)

def translate_text(text, dest):
    if dest.lower() == "english":
        return text
    try:
        translated = translator.translate(text, dest=dest.lower())
        return translated.text
    except Exception:
        return text

# Auth Session
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
    st.session_state['phone'] = ""

if not st.session_state['auth']:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Login")
    phone = st.sidebar.text_input("Phone")
    if st.sidebar.button("Login"):
        if phone:
            st.session_state['auth'] = True
            st.session_state['phone'] = phone
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Enter your phone number to login")
else:
    st.sidebar.markdown(f"Logged in as: {st.session_state['phone']}")
    if st.sidebar.button("Logout"):
        st.session_state['auth'] = False
        st.session_state['phone'] = ""

# Main Page Logic
if menu == "Home":
    st.title(translate_text("Welcome to AgriVoice Classifieds", lang))
    st.write(translate_text("Buy and sell agricultural products using voice in your language!", lang))

elif menu == "Post Product (Voice)":
    st.header(translate_text("Post Product via Voice", lang))
    audio = st.file_uploader("Upload voice recording (.wav)", type=["wav"])
    if audio and st.button("Post Product"):
        files = {'file': (audio.name, audio, audio.type)}
        response = requests.post(f"{BACKEND_URL}/voice-post", files=files)
        if response.ok:
            st.success(translate_text("Product posted successfully!", lang))
            st.json(response.json())
        else:
            st.error(translate_text("Failed to post product.", lang))

elif menu == "Register (Voice)":
    st.header(translate_text("Register via Voice", lang))
    reg_audio = st.file_uploader("Upload registration audio (.wav)", type=["wav"])
    if reg_audio and st.button("Register"):
        files = {'file': (reg_audio.name, reg_audio, reg_audio.type)}
        response = requests.post(f"{BACKEND_URL}/register-voice", files=files)
        if response.ok:
            st.success(translate_text("Registration successful!", lang))
            st.json(response.json())
        else:
            st.error(translate_text("Failed to register.", lang))

elif menu == "Search Products":
    st.header(translate_text("Search Products", lang))
    query = st.text_input(translate_text("Enter search query", lang))
    if st.button(translate_text("Search", lang)) and query:
        response = requests.get(f"{BACKEND_URL}/search", params={"query": query})
        if response.ok:
            result = response.json()
            for item in result.get("results", []):
                st.markdown(f"{item['name']} - ₦{item['price']} @ {item['location']}")
            if result.get("audio_url"):
                st.audio(result["audio_url"], format="audio/mp3")
        else:
            st.error(translate_text("Search failed.", lang))

elif menu == "Settings":
    st.subheader(translate_text("Settings", lang))
    st.markdown(translate_text("Here you can adjust preferences and language options.", lang))

# Audio Upload Section (outside navigation)
st.title("🎙️ FarmDepot.ai - Audio Upload")
uploaded_file = st.file_uploader("Upload your voice command", type=["wav", "mp3", "ogg"])
if uploaded_file:
    with st.spinner("Uploading and processing audio..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{BACKEND_URL}/upload-audio/", files=files)
        if response.ok:
            st.success("Audio uploaded and converted successfully!")
            st.json(response.json())
        else:
            st.error("Failed to process audio.")



