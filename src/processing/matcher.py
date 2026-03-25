from difflib import SequenceMatcher

MATCH_THRESHOLD = 0.60


def _similarity(a, b):
    """Return similarity ratio between two strings, case-insensitive."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _strip_extension(filename):
    """Remove file extension for cleaner matching (e.g. 'HW3.pdf' -> 'HW3')."""
    if "." in filename:
        return filename.rsplit(".", 1)[0]
    return filename


def match_files_to_tasks(tasks, drive_tasks):
    """
    For each Google Task, find Drive files whose name is similar to the task name.
    Mutates task.matched_files in place. Returns the tasks list.
    """
    task_items = [t for t in tasks if t.source == "task"]

    for task in task_items:
        matched = []
        for drive_task in drive_tasks:
            clean_name = _strip_extension(drive_task.name)
            ratio = _similarity(task.name, clean_name)
            if ratio >= MATCH_THRESHOLD:
                matched.append((drive_task.name, ratio))

        matched.sort(key=lambda x: x[1], reverse=True)
        task.matched_files = [name for name, _ in matched]

    return tasks
