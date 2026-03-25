from datetime import datetime
from src.models.task import Task


def normalize_tasks(raw_tasks):
    """Normalize Google Calendar Tasks into Task objects."""
    tasks = []
    for t in raw_tasks:
        if t.get("status") == "completed":
            continue

        name = t.get("title", "Untitled Task")
        task_id = t.get("id")
        list_title = t.get("_list_title")

        due = t.get("due")
        if due:
            deadline = datetime.fromisoformat(due.replace("Z", "+00:00"))
        else:
            deadline = None

        tasks.append(Task(
            name=name,
            deadline=deadline,
            source="task",
            task_id=task_id,
            list_title=list_title,
        ))
    return tasks


def normalize_calendar(events):
    """Normalize calendar events. These are meetings/classes — lower priority."""
    tasks = []
    for e in events:
        name = e.get("summary", "Untitled Event")
        task_id = e.get("id")

        start = e.get("start", {}).get("dateTime")
        if start:
            event_time = datetime.fromisoformat(start.replace("Z", "+00:00"))
        else:
            event_time = None

        tasks.append(Task(
            name=name,
            deadline=event_time,
            source="event",
            task_id=task_id,
            event_time=event_time,
        ))
    return tasks


def normalize_drive(files):
    """Normalize Drive files. Used for correlation with tasks."""
    tasks = []
    for f in files:
        name = f.get("name")
        task_id = f.get("id")
        modified = f.get("modifiedTime")
        if modified:
            last_updated = datetime.fromisoformat(modified.replace("Z", "+00:00"))
        else:
            last_updated = None
        tasks.append(Task(
            name=name,
            last_updated=last_updated,
            source="drive",
            task_id=task_id,
        ))
    return tasks
