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
    # Missing doc: 内部函数缺少文档
    return "This is internal"
