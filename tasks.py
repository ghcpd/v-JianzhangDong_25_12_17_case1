"""Task related models and manager.

Provides Task model and TaskManager to manage tasks in memory.
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
        """Mark this task as completed by setting status to 'done'."""
        self.status = "done"

class TaskManager:
    """Manage a collection of Task objects in memory."""
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a Task to the manager."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """Return a list of all managed tasks."""
        return self.tasks

    def remove_task(self, index: int):
        """Remove a task by its index if it exists."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
