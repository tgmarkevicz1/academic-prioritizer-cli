class Task:
    def __init__(self, name, deadline=None, last_updated=None, source=None):
        self.name = name
        self.deadline = deadline
        self.last_updated = last_updated
        self.source = source

    def __repr__(self):
        return f"<Task {self.name}>"
