import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client

#loading environment variables

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in .env"
    )

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

#fastapi application

app = FastAPI(
    title = "Auth Login & Protect API",
    description = "Secure API using FastAPI and Supabase Auth",
    version = "1.0.0"
)

#request models
class AuthRequest(BaseModel):
    email:EmailStr
    password: str

#HTTP bearer security

security = HTTPBearer()


#authentication dependency

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)

):
    "Extracts the Bearer token and verifies it with Supabase."

    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIzed,
            detail={"error": "Access token required"}
        )
    try:
        #verify token with Supabase

        response = supabase.auth.get_user(token)
        user = response.user
        if user in None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = {"error": "Invalid or expired token"}
            )
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHorized,
            detail = {"error": "Invalid or expired token"}
        )

#Public route

@app.get("/public/info")
def public_info():
    return {
        "message":"Welcome stranger! This info is public"
    }

#sign up

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(data: AuthRequest):

    try:
        response = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password
            }
        )

        user = response.user

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Unable to create user"
                }
            )

        return {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": str(e)
            }
        )

#login

@app.post("/auth/login")
def login(data: AuthRequest):

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password
            }
        )

        if response.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid login credentials"
                }
            )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid login credentials"
            }
        )

#protected profile
@app.get("/protected/profile")
def profile(user=Depends(get_current_user)):

    return {
        "message": "You have accessed a protected route",
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
    }
#protected dashboard

@app.get("/protected/dashboard")
def dashboard(user=Depends(get_current_user)):

    return {
        "message": "Welcome to your protected dashboard",
        "user_id": user.id
    }

#logout

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        # Supabase Python SDK signs out the current client session.
        # We first verify that the supplied token belongs to a valid user.
        supabase.auth.get_user(token)

        return None

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid or expired token"
            }
        )