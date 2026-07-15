from pathlib import Path

from task_manager_api.database import (
    db_init,
    save_db,
    get_all_tasks,
    delete_task_from_db,
    get_task_by_id,
    patch_task_by_id
)

from fastapi import FastAPI, HTTPException, status
from .models import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI()

Path("data").mkdir(exist_ok=True)
DB_PATH = Path("data") / "tasks.db"

db_init(DB_PATH)

id_count = 1


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate):
    return save_db(DB_PATH, data)


@app.get("/tasks", response_model=list[TaskResponse])
def show_tasks():
    task_list = get_all_tasks(DB_PATH)
    return task_list


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def show_task_by_id(task_id: int):
    task = get_task_by_id(DB_PATH, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    return task


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int):
    task = get_task_by_id(DB_PATH, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    delete_task_from_db(DB_PATH, task_id)

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(data: TaskUpdate, task_id: int):
    task = get_task_by_id(DB_PATH, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    changes = data.model_dump(exclude_unset=True)

    patch_task_by_id(DB_PATH, task_id, changes)

    new_task = get_task_by_id(DB_PATH, task_id)

    return new_task
