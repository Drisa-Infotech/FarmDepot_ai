import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

class Settings:
    # PostgreSQL DB URL
    DB_URL = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # OpenRouter AI API Config
    OPENROUTER_API_BASE_URL = os.getenv("OPENROUTER_API_BASE_URL")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # App settings
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Audio Upload Directory
    AUDIO_UPLOAD_DIR = os.getenv("AUDIO_UPLOAD_DIR", "static/audios")

    # DeepL or Google Translate Key (for translation)
DEEPL_API_KEY= os.getenv("DEEPL_API_KEY")

settings = Settings()
