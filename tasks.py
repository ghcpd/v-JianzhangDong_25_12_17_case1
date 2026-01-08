"""Task models and a manager for handling tasks.

This module provides the Task data structure and the TaskManager which
allows adding, listing and removing tasks.
"""

from typing import List

class Task:
    """Represents a single task with title, description and status."""
    def __init__(self, title: str, description: str, status: str = "pending"):
        self.title = title
        self.description = description
        self.status = status

    def mark_done(self):
        """Mark the task as done by updating its status value."""
        self.status = "done"

class TaskManager:
    """Manager for Task objects providing add/list/remove operations."""
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a Task instance to the manager."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """Return the list of all stored Task instances."""
        return self.tasks

    def remove_task(self, index: int):
        """Remove a task by index if the index is valid."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
