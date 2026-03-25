from datetime import datetime, timezone


def score(task):
    now = datetime.now(timezone.utc)
    s = 0

    if task.source == "task":
        if task.deadline:
            days_left = (task.deadline - now).days
            s += max(0, 15 - days_left)
        else:
            s += -2

        match_bonus = min(len(task.matched_files), 2) * 3
        s += match_bonus

    elif task.source == "event":
        if task.event_time:
            days_until = (task.event_time - now).days
            s = -100 + max(0, 7 - days_until)
        else:
            s = -100

    elif task.source == "drive":
        s = 0

    return s
