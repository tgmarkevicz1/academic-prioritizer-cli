from .google_auth import get_service


def get_task_lists(service):
    """Return all task lists for the authenticated user."""
    result = service.tasklists().list().execute()
    return result.get("items", [])


def get_tasks_from_list(service, tasklist_id):
    """Return all incomplete tasks from a given task list."""
    tasks = []
    page_token = None

    while True:
        result = service.tasks().list(
            tasklist=tasklist_id,
            showCompleted=False,
            showHidden=False,
            pageToken=page_token,
        ).execute()

        for item in result.get("items", []):
            if item.get("status") == "completed":
                continue
            tasks.append(item)

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    return tasks


def get_all_tasks():
    """Fetch all incomplete tasks across all task lists."""
    service = get_service("tasks", "v1")
    all_tasks = []

    for task_list in get_task_lists(service):
        list_id = task_list["id"]
        list_title = task_list.get("title", "My Tasks")
        tasks = get_tasks_from_list(service, list_id)
        for task in tasks:
            task["_list_title"] = list_title
        all_tasks.extend(tasks)

    return all_tasks
