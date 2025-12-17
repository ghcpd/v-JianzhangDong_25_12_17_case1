"""Task management module."""

from typing import List

class Task:
    """
    任务类，包含任务的基本信息
    """
    def __init__(self, title: str, description: str, status: str = "pending"):
        """Initialize a task with title, description, and status."""
        self.title = title
        self.description = description
        self.status = status

    def mark_done(self):
        """Mark the task as done."""
        self.status = "done"

class TaskManager:
    """Manages a collection of tasks."""
    def __init__(self):
        """Initialize the task manager."""
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to the manager."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """List all tasks."""
        return self.tasks

    def remove_task(self, index: int):
        """Remove a task by index."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
