from fastapi import FastAPI, UploadFile, File
from agents.voice_agent import voice_agent
from agents.post_agent import post_agent
from agents.search_agent import search_agent
from agents.register_agent import register_agent
from agents.support_agent import support_agent
from tasks.voice_tasks import process_voice_input, extract_product_details, text_to_speech
from tasks.classified_tasks import post_product, search_products
from tasks.register_tasks import register_user_voice

app = FastAPI(title="FarmDepot.ai")

@app.get("/")
def root():
    return {"message": "Welcome to FarmDepot.ai - An AI-Powered Classified Ads for anything Agriculture"}

@app.post("/voice-input")
def voice_input(audio: UploadFile = File(...)):
    return process_voice_input(audio)

@app.post("/post-product-voice")
def post_product_from_voice(audio: UploadFile = File(...)):
    product_data = extract_product_details(audio)
    return post_product(product_data)

@app.post("/post-product")
def post_product_route(data: dict):
    return post_product(data)

@app.get("/search")
def search_product_route(query: str):
    result = search_products(query)
    result_text = "\n".join([f"{p['quantity']} of {p['name']} for ₦{p['price']} in {p['location']}" for p in result["results"]])
    voice_path = text_to_speech(result_text)
    return {"result": result, "voice_summary": voice_path}

@app.post("/register-voice")
def register_voice_user(audio: UploadFile = File(...)):
    return register_user_voice(audio)
    
