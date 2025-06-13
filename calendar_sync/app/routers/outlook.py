from fastapi import APIRouter, HTTPException
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
def outlook_auth():
    if not settings.outlook_client_id:
        raise HTTPException(status_code=500, detail="OUTLOOK_CLIENT_ID is not configured")
    base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": settings.outlook_client_id,
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
    if not settings.outlook_client_secret:
        raise HTTPException(status_code=500, detail="OUTLOOK_CLIENT_SECRET is not configured")
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": settings.outlook_client_id,
        "client_secret": settings.outlook_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/outlook/callback",
        "scope": "https://graph.microsoft.com/Calendars.ReadWrite"
    }
    response = httpx.post(token_url, data=data)
    token_data = response.json()

    session = SessionLocal()
    expires_at = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 0))
    token = Token(
        provider="outlook",
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
    token = session.query(Token).filter_by(provider="outlook").first()
    if not token:
        session.close()
        return JSONResponse({"error": "not authenticated"}, status_code=400)

    headers = {"Authorization": f"Bearer {token.access_token}"}
    resp = httpx.get(
        "https://graph.microsoft.com/v1.0/me/calendar/events",
        headers=headers,
    )
    session.close()
    return JSONResponse(resp.json())


