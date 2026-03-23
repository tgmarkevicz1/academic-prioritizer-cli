from .google_auth import get_service
from datetime import datetime, timedelta

def get_calendar_events():
    service = get_service("calendar", "v3")

    now = datetime.utcnow().isoformat() + "Z"
    week = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"

    events = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=week,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events.get("items", [])
