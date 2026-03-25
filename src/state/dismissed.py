import json
import os

DISMISSED_PATH = os.path.expanduser("~/.academic_prioritizer_dismissed.json")


def _load():
    if not os.path.exists(DISMISSED_PATH):
        return {}
    try:
        with open(DISMISSED_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data):
    with open(DISMISSED_PATH, "w") as f:
        json.dump(data, f, indent=2)


def hide(task_id, label=""):
    data = _load()
    data[task_id] = label
    _save(data)


def unhide(task_id):
    data = _load()
    if task_id in data:
        del data[task_id]
        _save(data)
        return True
    return False


def is_hidden(task_id):
    data = _load()
    return task_id in data


def get_all_hidden():
    return _load()


def filter_hidden(tasks):
    data = _load()
    return [t for t in tasks if t.task_id not in data]
