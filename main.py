from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import openai
import tempfile

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

app = FastAPI(title="Gramin GPT - Backend")

class ChatRequest(BaseModel):
    text: str
    lang: str = "en"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured on server.")
    prompt = f"""You are Gramin GPT, a friendly assistant for rural users. Respond in simple {req.lang} and keep answers short and actionable.
User: {req.text}
"""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2,
        )
        answer = resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"reply": answer}

@app.post("/api/summarize")
async def summarize(text: str = Form(...)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured on server.")
    prompt = f"""Summarize the following medical or technical text into simple language (2-3 short sentences). Text:\n{text}
Return only the summary.
"""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.2,
        )
        summary = resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"summary": summary}

@app.post('/api/upload_report')
async def upload_report(file: UploadFile = File(...), user_id: str = Form(...)):
    ext = os.path.splitext(file.filename)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    contents = await file.read()
    tmp.write(contents)
    tmp.flush()
    tmp.close()
    return {"status": "uploaded", "path": tmp.name, "filename": file.filename}
