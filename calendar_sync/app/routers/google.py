from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os
import urllib.parse
import httpx

router = APIRouter()

@router.get("/auth")
def google_auth():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": "http://localhost:8000/google/callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
def google_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": "http://localhost:8000/google/callback",
        "grant_type": "authorization_code"
    }
    response = httpx.post(token_url, data=data)
    return JSONResponse(response.json())
