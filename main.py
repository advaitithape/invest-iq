from fastapi import FastAPI
from backend.authentication.routes import router
from backend.chatbot.bot import router as bot_router

app = FastAPI()

app.include_router(router)
app.include_router(bot_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Finance Website API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
