import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase
cred = credentials.Certificate("backend/authentication/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

