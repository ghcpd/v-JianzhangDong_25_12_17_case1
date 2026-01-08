"""FastAPI application that exposes endpoints for task management."""

from fastapi import FastAPI
from tasks import Task, TaskManager

app = FastAPI()
manager = TaskManager()

@app.get("/tasks")
def get_tasks():
    """Return a list of titles for all stored tasks."""
    return [task.title for task in manager.list_tasks()]

@app.post("/tasks")
def create_task(title: str, description: str):
    """Create a new task with the given title and description.

    Args:
        title: The title of the task.
        description: The detailed description of the task.

    Returns:
        A JSON dictionary indicating success.
    """
    task = Task(title, description)
    manager.add_task(task)
    return {"message": "Task added successfully"}


def internal_helper():
    """Internal helper returning a simple string; not part of the public API."""
    return "This is internal"
