from fastapi import FastAPI, HTTPException
from .models import TaskCreate, TaskUpdate

app = FastAPI()

task_list = []

id_count = 1


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/tasks")
def create_task(data: TaskCreate):
    global id_count

    new_task = {
        "id": id_count,
        "title": data.title,
        "description": data.description,
        "due_date": data.due_date,
    }

    task_list.append(new_task)

    id_count += 1

    return new_task


@app.get("/tasks")
def show_tasks():
    return task_list


@app.get("/tasks/{task_id}")
def show_task_by_id(task_id: int):
    task = next((task for task in task_list if task["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = next((task for task in task_list if task["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    task_list.remove(task)

    return task


@app.patch("/tasks/{task_id}")
def patch_task(data: TaskUpdate, task_id: int):
    task = next((task for task in task_list if task["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="No task found")

    changes = data.model_dump(exclude_unset=True)

    task.update(changes)

    return task
