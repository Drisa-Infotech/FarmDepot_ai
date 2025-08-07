### agri_voice_classified/tasks/voice_tasks.py
import whisper
from gtts import gTTS
import tempfile
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model = whisper.load_model("base")
translator = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

extract_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Extract the following details from the text:
- Product Name
- Quantity
- Price per unit (in Naira)
- Location

Text: {text}

Respond in JSON format with keys: name, quantity, price, location.
"""
)
extract_chain = LLMChain(llm=translator, prompt=extract_prompt)

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
    response = extract_chain.run(text=user_text)
    return eval(response)  # JSON-like string

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        return f.name
