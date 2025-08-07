
import requests
import os

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def translate_text(text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    data = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]
