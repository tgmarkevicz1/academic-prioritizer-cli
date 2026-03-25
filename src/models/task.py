class Task:
    def __init__(
        self,
        name,
        deadline=None,
        last_updated=None,
        source=None,
        task_id=None,
        event_time=None,
        matched_files=None,
        list_title=None,
    ):
        self.name = name
        self.deadline = deadline
        self.last_updated = last_updated
        self.source = source
        self.task_id = task_id
        self.event_time = event_time
        self.matched_files = matched_files or []
        self.list_title = list_title

    def __repr__(self):
        return f"<Task {self.name!r} source={self.source}>"
