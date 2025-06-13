from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os
import urllib.parse
import httpx
from datetime import datetime, timedelta
from ...db import SessionLocal
from ...models import Token
from ...config import settings

router = APIRouter()

@router.get("/auth")
def google_auth():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.google_client_id,
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
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": "http://localhost:8000/google/callback",
        "grant_type": "authorization_code"
    }
    response = httpx.post(token_url, data=data)
    token_data = response.json()

    session = SessionLocal()
    expires_at = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 0))
    token = Token(
        provider="google",
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_at=expires_at,
    )
    session.add(token)
    session.commit()
    session.close()
    return JSONResponse({"status": "token stored"})


@router.get("/events")
def list_events():
    session = SessionLocal()
    token = session.query(Token).filter_by(provider="google").first()
    if not token:
        session.close()
        return JSONResponse({"error": "not authenticated"}, status_code=400)

    headers = {"Authorization": f"Bearer {token.access_token}"}
    resp = httpx.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers=headers,
    )
    session.close()
    return JSONResponse(resp.json())


