from datetime import datetime, timezone

def score(task):
    score = 0
    now = datetime.now(timezone.utc) 

    # Deadline proximity
    if task.deadline:
        days_left = (task.deadline - now).days
        score += max(0, 10 - days_left)

    # Inactivity
    if task.last_updated:
        days_idle = (now - task.last_updated).days
        score += days_idle

    return score
