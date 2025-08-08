
import whisper
from gtts import gTTS
import tempfile
from sqlalchemy import create_engine
from config import settings
import os
import json
from backend.utils.openrouter_api import openrouter_chat

# Init DB connection
engine = create_engine(settings.DB_URL)

# Load Whisper model
model = whisper.load_model("base")

def process_voice_input(audio_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_file.file.read())
            temp_audio_path = temp_audio.name

        result = model.transcribe(temp_audio_path)
        text = result["text"]

        response = f"You said: {text}"
        tts = gTTS(text=response, lang='en')
        tts_path = temp_audio_path.replace(".wav", "_response.mp3")
        tts.save(tts_path)

        return {"transcription": text, "response_audio_path": tts_path}

    except Exception as e:
        return {"error": str(e)}

def extract_product_details(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.file.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    user_text = result["text"]
    
    messages = [
        {
            "role": "system",
            "content": "Extract the following product details from the input as JSON with keys: name, quantity, price, location."
        },
        {"role": "user", "content": user_text}
    ]

    response = openrouter_chat(messages)
    return json.loads(response['choices'][0]['message']['content'])

def extract_details_with_openrouter(text):
    messages = [
        {
            "role": "system",
            "content": "Extract the following details from the text: Product Name, Quantity, Price per unit (in Naira), Location. Respond in JSON format with keys: name, quantity, price, location."
        },
        {"role": "user", "content": text}
    ]
    response = openrouter_chat(messages)
    return json.loads(response['choices'][0]['message']['content'])

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        return f.name

from backend.utils.audio_utils import (
    transcribe_audio,
    synthesize_speech
)

from backend.utils.translation_utils import (
    translate_text
)

# Transcription Task
def transcribe_audio_task(audio_file_path: str, language: str = "en") -> str:
    """
    Transcribes the given audio file using Whisper via OpenRouter.
    """
    return transcribe_audio(audio_file_path, language)

# TTS Task
def text_to_speech_task(text: str, language: str = "en", voice: str = "default") -> str:
    """
    Converts text to speech using OpenRouter TTS (or any backend you configure).
    Returns the path to the generated audio file.
    """
    return synthesize_speech(text, language, voice)

# Translation Task
def translate_text_task(text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    """
    Translates the input text to the target language.
    """
    return translate_text(text, source_lang, target_lang)
