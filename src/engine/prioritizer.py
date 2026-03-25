from src.processing.scorer import score


def prioritize(tasks):
    """Sort tasks by score descending. Drive files are excluded from display."""
    displayable = [t for t in tasks if t.source in ("task", "event")]
    return sorted(displayable, key=lambda t: score(t), reverse=True)
