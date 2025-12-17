"""HTTP API definitions for a tiny task service.

Defines a couple of lightweight endpoints used by the example app and
kept intentionally simple for demonstration and tests.
"""

from fastapi import FastAPI
from tasks import Task, TaskManager

app = FastAPI()
manager = TaskManager()

@app.get("/tasks")
def get_tasks():
    """
    获取所有任务
    """
    return [task.title for task in manager.list_tasks()]

@app.post("/tasks")
def create_task(title: str, description: str):
    """Create a new task given a title and description.

    Adds the created Task to the module-level TaskManager instance and
    returns a simple success message dictionary.
    """
    task = Task(title, description)
    manager.add_task(task)
    return {"message": "Task added successfully"}

def internal_helper():
    """Internal helper used by some examples; intentionally trivial."""
    return "This is internal"
