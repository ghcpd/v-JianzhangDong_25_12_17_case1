"""Task data structures and management helpers.

This module defines a simple Task data class and a TaskManager that
keeps tasks in memory and provides convenience methods to add, list
and remove tasks.
"""

from typing import List

class Task:
    """
    任务类，包含任务的基本信息
    """
    def __init__(self, title: str, description: str, status: str = "pending"):
        self.title = title
        self.description = description
        self.status = status

    def mark_done(self):
        """Mark this task as done by changing its status attribute."""
        self.status = "done"

class TaskManager:
    """In-memory manager for Task objects providing basic CRUD-like ops."""
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a Task instance to the manager's internal list."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """Return the list of managed Task objects."""
        return self.tasks

    def remove_task(self, index: int):
        """Remove the task at the given index if it exists."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
