"""API endpoints for managing tasks in the TaskManager.

This module exposes FastAPI endpoints to create and list tasks.
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
    """Create a new task with the given title and description."""
    task = Task(title, description)
    manager.add_task(task)
    return {"message": "Task added successfully"}

def internal_helper():
    """Internal helper used for internal operations."""
    return "This is internal"
