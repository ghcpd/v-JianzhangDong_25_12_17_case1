"""Task management module.
Contains Task and TaskManager classes for managing application tasks.
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
        self.status = "done"

class TaskManager:
    """Manager class for handling collections of tasks.
    
    Provides methods for adding, listing, and removing tasks from the task collection.
    """
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def list_tasks(self) -> list:
        return self.tasks

    def remove_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
