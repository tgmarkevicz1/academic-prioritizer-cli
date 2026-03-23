from datetime import datetime
from src.models.task import Task

def normalize_calendar(events):
    tasks = []
    for e in events:
        name = e.get("summary", "Untitled Event")
        start = e.get("start", {}).get("dateTime")
        if start:
            deadline = datetime.fromisoformat(start.replace("Z", "+00:00"))
        else:
            deadline = None
        tasks.append(Task(name=name, deadline=deadline, source="calendar"))
    return tasks


def normalize_drive(files):
    tasks = []
    for f in files:
        name = f.get("name")
        modified = f.get("modifiedTime")
        if modified:
            last_updated = datetime.fromisoformat(modified.replace("Z", "+00:00"))
        else:
            last_updated = None
        tasks.append(Task(name=name, last_updated=last_updated, source="drive"))
    return tasks
