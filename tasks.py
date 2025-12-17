"""Task models and manager for the application."""

from typing import List

class Task:
    """Represents a task with a title, description, and status."""
    def __init__(self, title: str, description: str, status: str = "pending"):
        """Initialize a new Task.

        Args:
            title (str): Title of the task.
            description (str): Description of the task.
            status (str, optional): Initial status. Defaults to "pending".
        """
        self.title = title
        self.description = description
        self.status = status

    def mark_done(self):
        """Mark the task as completed by setting status to 'done'."""
        self.status = "done"

class TaskManager:
    def __init__(self):
        """Initialize a TaskManager with an empty list of tasks."""
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a Task to the manager's list of tasks."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """Return the list of tasks managed."""
        return self.tasks

    def remove_task(self, index: int):
        """Remove a task from the list by its index if it exists.

        Args:
            index (int): Index of the task to remove.
        """
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
