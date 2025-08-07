## agri_voice_classified/tasks/register_tasks.py
import whisper
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from db.models import User
from db.session import SessionLocal
import tempfile

model = whisper.load_model("base")
translator = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

register_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Extract user registration details from the text:
- Full name
- Phone number
- Location

Text: {text}

Respond in JSON format with keys: name, phone, location.
"""
)
register_chain = LLMChain(llm=translator, prompt=register_prompt)

def register_user_voice(audio_file):
    db = SessionLocal()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.file.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    text = result["text"]
    data = eval(register_chain.run(text=text))

    user = User(name=data['name'], phone=data['phone'], location=data['location'])
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user": data}
