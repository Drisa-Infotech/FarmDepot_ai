
import whisper
from db.models import User
from sqlalchemy.orm import sessionmaker
import tempfile
from sqlalchemy import create_engine
from config import settings
import os
import json

from utils.openrouter_api import openrouter_chat  # <-- Use the new utility

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(bind=engine)

model = whisper.load_model("base")

def register_user_voice(audio_file):
    db = SessionLocal()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.file.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    text = result["text"]

    messages = [
        {
            "role": "system",
            "content": (
                "Extract user registration details from the text. "
                "Return a JSON object with keys: name, phone, location."
            )
        },
        {
            "role": "user",
            "content": text
        }
    ]
    response = openrouter_chat(messages)
    content = response['choices'][0]['message']['content']
    data = json.loads(content)

    user = User(name=data['name'], phone=data['phone'], location=data['location'])
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user": data}
