import firebase_admin
from firebase_admin import auth, credentials
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Initialize Firebase Admin SDK (Make sure the path to your JSON key is correct)
cred = credentials.Certificate("backend/authentication/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Pydantic model for user signup
class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def signup(user: SignupRequest):
    try:
        # Create a new user in Firebase Authentication
        firebase_user = auth.create_user(email=user.email, password=user.password)
        return {"message": "User signed up successfully", "uid": firebase_user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
