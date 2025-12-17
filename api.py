"""API module for FastAPI application.
Provides endpoints for task management operations.
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
    task = Task(title, description)
    manager.add_task(task)
    return {"message": "Task added successfully"}

def internal_helper():
    """Internal helper function for API operations.
    
    Returns:
        str: A status message for internal use.
    """
    return "This is internal"
