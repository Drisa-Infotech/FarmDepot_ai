import os
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment

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

