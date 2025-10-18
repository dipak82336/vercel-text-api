from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from vercel_kv import kv
from dotenv import load_dotenv

# Vercel પર્યાવરણ ચલોને લોડ કરવા માટે
load_dotenv()

app = FastAPI()

@app.post("/api/send_text")
async def send_text_handler(request: Request):
    try:
        data = await request.json()
        new_text = data.get('text')

        if new_text is not None:
            # Vercel KV માં 'current_text' કીની વેલ્યુ સેટ કરો
            kv.set("current_text", new_text)
            return JSONResponse(content={"message": "Text updated successfully!"})
        else:
            return JSONResponse(content={"error": "Text not provided"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
