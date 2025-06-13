from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os
import urllib.parse
import httpx

router = APIRouter()

@router.get("/auth")
def outlook_auth():
    base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": os.getenv("OUTLOOK_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": "http://localhost:8000/outlook/callback",
        "response_mode": "query",
        "scope": "https://graph.microsoft.com/Calendars.ReadWrite",
        "prompt": "consent"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
def outlook_callback(code: str):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": os.getenv("OUTLOOK_CLIENT_ID"),
        "client_secret": os.getenv("OUTLOOK_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/outlook/callback",
        "scope": "https://graph.microsoft.com/Calendars.ReadWrite"
    }
    response = httpx.post(token_url, data=data)
    return JSONResponse(response.json())
