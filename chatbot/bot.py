from fastapi import APIRouter, HTTPException
import requests
from google.cloud import bigquery
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

BIG_QUERY_ID = 'smiling-sweep-450612-g4'
BIG_QUERY_DATASET = 'user_credentials'
BIG_QUERY_TABLE = 'chat_history'

GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

class ChatRequest(BaseModel):
    user_id: str
    message: str

def store_chat_history(user_id, message, reply):
    client = bigquery.Client()
    table_id = f"{BIG_QUERY_ID}.{BIG_QUERY_DATASET}.{BIG_QUERY_TABLE}"

    rows_to_insert = [{
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "reply": reply
    }]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"Error inserting chat history: {errors}")
    else:
        print("Chat history stored successfully!")


@router.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not found")

    payload = {
        "contents": [{"parts": [{"text": message}]}]
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")

    store_chat_history(request.user_id, request.message, reply)

    return {"reply": reply}
