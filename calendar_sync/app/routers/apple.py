"""Apple Calendar endpoints using CalDAV."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ...config import settings
import caldav

router = APIRouter()


def _get_client():
    if not (settings.apple_caldav_url and settings.apple_username and settings.apple_password):
        raise RuntimeError("Apple CalDAV credentials are not configured")
    return caldav.DAVClient(
        url=settings.apple_caldav_url,
        username=settings.apple_username,
        password=settings.apple_password,
    )


@router.get("/events")
def list_events():
    """Return upcoming events from the first calendar."""
    try:
        client = _get_client()
        principal = client.principal()
        calendars = principal.calendars()
        if not calendars:
            return JSONResponse({"events": []})
        cal = calendars[0]
        events = []
        for event in cal.events():
            try:
                vevent = event.vobject_instance.vevent
                events.append({
                    "uid": getattr(vevent, "uid", {}).value,
                    "summary": getattr(vevent, "summary", {}).value,
                    "start": str(getattr(vevent, "dtstart", {}).value),
                })
            except Exception:
                continue
        return JSONResponse({"events": events})
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)
