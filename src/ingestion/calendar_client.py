from .google_auth import get_service
from datetime import datetime, timedelta, timezone


def get_calendar_events():
    service = get_service("calendar", "v3")

    now = datetime.now(timezone.utc).isoformat()
    week = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    all_events = []

    # 1. Get all calendars
    calendars = service.calendarList().list().execute()

    for cal in calendars.get("items", []):
        calendar_id = cal["id"]

        # 2. Get events from each calendar
        events = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=week,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        # 3. Add calendar name for context (optional but useful)
        for event in events.get("items", []):
            event["calendar"] = cal.get("summary", "Unknown")

        all_events.extend(events.get("items", []))

    # Optional: sort everything together
    all_events.sort(
        key=lambda e: e["start"].get("dateTime", e["start"].get("date"))
    )

    return all_events
