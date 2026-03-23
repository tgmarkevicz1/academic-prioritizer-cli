from .google_auth import get_service
from datetime import datetime, timedelta, timezone

def get_calendar_events():
    service = get_service("calendar", "v3")

    now = datetime.now(timezone.utc).isoformat()
    week = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    events = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=week,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events.get("items", [])
