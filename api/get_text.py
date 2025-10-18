from fastapi import FastAPI
from fastapi.responses import JSONResponse
from vercel_kv import kv
from dotenv import load_dotenv

# Vercel પર્યાવરણ ચલોને લોડ કરવા માટે
load_dotenv()

app = FastAPI()

@app.get("/api/get_text")
def get_text_handler():
    # Vercel KV માંથી 'current_text' કીની વેલ્યુ મેળવો
    # જો કોઈ વેલ્યુ ન હોય, તો "Default text" બતાવો
    current_text = kv.get("current_text") or "Default text"
    return JSONResponse(content={"text": current_text})
