import os
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
import streamlit as st
import requests

st.set_page_config(page_title="FarmDepot.ai - Voice-Powered Agri Marketplace", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🌾 FarmDepot.ai - Voice-Powered Agri Marketplace")

st.sidebar.header("🎙️ Voice & Language Tools")

# Ensure the directory exists
AUDIO_DIR = os.path.join("static", "audios")
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_filename(prefix="audio", extension="mp3"):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}_{timestamp}.{extension}"

def save_uploaded_audio(file, save_dir='static/audios'):
    """Save uploaded audio file and return file path."""
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return file_path

def convert_to_wav(input_path):
    """Convert audio file to WAV format for compatibility."""
    if input_path.endswith(".wav"):
        return input_path
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")
    return output_path

def convert_text_to_speech(text, lang='en', filename=None):
    """Convert given text to speech and save as MP3"""
    if not filename:
        filename = generate_filename(prefix="tts", extension="mp3")
    filepath = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    return filepath

def convert_audio_format(src_path, target_format="mp3"):
    """Convert uploaded audio to target format (e.g., WAV to MP3)"""
    audio = AudioSegment.from_file(src_path)
    target_filename = os.path.splitext(os.path.basename(src_path))[0] + f".{target_format}"
    target_path = os.path.join(AUDIO_DIR, target_filename)
    audio.export(target_path, format=target_format)
    return target_path

def list_audio_files():
    """Return a list of all audio files in the static/audios/ directory"""
    return [f for f in os.listdir(AUDIO_DIR) if os.path.isfile(os.path.join(AUDIO_DIR, f))]

# === Audio Upload for Transcription ===
st.sidebar.subheader("1. Transcribe Audio")
audio_file = st.sidebar.file_uploader("Upload an audio file (mp3, wav)", type=["mp3", "wav"])
if audio_file and st.sidebar.button("Transcribe"):
    files = {"file": (audio_file.name, audio_file, audio_file.type)}
    res = requests.post(f"{BACKEND_URL}/transcribe", files=files)
    if res.status_code == 200:
        st.sidebar.success("Transcription:")
        st.sidebar.write(res.json()["text"])
    else:
        st.sidebar.error("Transcription failed.")

# === TTS ===
st.sidebar.subheader("2. Text-to-Speech")
tts_text = st.sidebar.text_area("Enter text to convert to speech")
tts_lang = st.sidebar.text_input("Language code (e.g., en, ha, ig, yo)", value="en")
if tts_text and st.sidebar.button("Generate Audio"):
    payload = {"text": tts_text, "lang": tts_lang}
    res = requests.post(f"{BACKEND_URL}/text-to-speech", json=payload)
    if res.status_code == 200:
        audio_path = res.json()["audio_url"]
        st.sidebar.audio(f"{BACKEND_URL}/{audio_path}", format="audio/mp3")
    else:
        st.sidebar.error("TTS failed.")

# === Translation ===
st.sidebar.subheader("3. Translate Text")
text_to_translate = st.sidebar.text_area("Enter text to translate")
source_lang = st.sidebar.text_input("Source language (e.g., en, ha)", value="en")
target_lang = st.sidebar.text_input("Target language (e.g., yo, ig)", value="yo")
if text_to_translate and st.sidebar.button("Translate"):
    payload = {
        "text": text_to_translate,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    res = requests.post(f"{BACKEND_URL}/translate", json=payload)
    if res.status_code == 200:
        st.sidebar.success("Translated:")
        st.sidebar.write(res.json()["translated_text"])
    else:
        st.sidebar.error("Translation failed.")

# === Classified Ads Section ===
st.header("📢 Post Agricultural Product")
st.write("Use voice or manual entry to post your agri product.")

with st.form("classified_form"):
    name = st.text_input("Product Name")
    description = st.text_area("Product Description")
    category = st.selectbox("Category", ["Grains", "Fruits", "Vegetables", "Tubers", "Livestock"])
    price = st.number_input("Price (₦)", min_value=0.0)
    contact = st.text_input("Contact Info")
    submitted = st.form_submit_button("Post Product")

if submitted:
    product = {
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "contact": contact
    }
    res = requests.post(f"{BACKEND_URL}/post-product", json=product)
    if res.status_code == 200:
        st.success("✅ Product posted successfully!")
    else:
        st.error("❌ Failed to post product.")

st.header("🔍 Browse Products")
res = requests.get(f"{BACKEND_URL}/products")
if res.status_code == 200:
    products = res.json()
    for p in products:
        with st.expander(f"{p['name']} - ₦{p['price']}"):
            st.write(f"**Category:** {p['category']}")
            st.write(f"**Description:** {p['description']}")
            st.write(f"**Contact:** {p['contact']}")
else:
    st.error("Could not load products.")
