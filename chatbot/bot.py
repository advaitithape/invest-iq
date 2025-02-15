from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Configure Gemini API
genai.configure(api_key="AIzaSyCHI7I4L21viPS3SjYNfqiHu7wIZrmmf0s")

app = FastAPI()

# Enable CORS so frontend can access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Frontend access)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request structure
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.message)

        return {"response": response.text}
    
    except Exception as e:
        return {"error": str(e)}

# Run FastAPI Server: uvicorn main:app --reload
