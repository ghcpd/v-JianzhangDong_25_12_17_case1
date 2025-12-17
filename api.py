"""API endpoints for task management."""

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
    """Create a new task and add it to the manager.

    Args:
        title (str): The title of the new task.
        description (str): The description of the new task.

    Returns:
        dict: A success message indicating the task was added.
    """
    task = Task(title, description)
    manager.add_task(task)
    return {"message": "Task added successfully"}

def internal_helper():
    """Internal helper function placeholder.

    Returns:
        str: A message describing the internal helper.
    """
    return "This is internal"
