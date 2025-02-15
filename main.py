from fastapi import FastAPI
from backend.authentication.routes import router as auth_router  # Import auth routes

app = FastAPI()

# Include authentication routes
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
