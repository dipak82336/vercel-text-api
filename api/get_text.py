from fastapi import FastAPI
from fastapi.responses import JSONResponse
from vercel_kv import kv

app = FastAPI()

@app.get("/api/get_text")
def get_text_handler():
    # સીધા Vercel ના સિસ્ટમ વેરીએબલ્સ પરથી કનેક્ટ થશે
    current_text = kv.get("current_text") or "Default text"
    return JSONResponse(content={"text": current_text})
