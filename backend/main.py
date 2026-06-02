from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4

app = FastAPI(title="Todo DevOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

todos = {}


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    status: Literal["pending", "active", "completed"] | None = None
    completed: bool | None = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/todos")
def get_todos():
    return list(todos.values())


@app.post("/todos")
def create_todo(todo: TodoCreate):
    todo_id = str(uuid4())
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "status": "pending",
        "completed": False,
    }
    todos[todo_id] = new_todo
    return new_todo


@app.patch("/todos/{todo_id}")
def update_todo(todo_id: str, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.title is not None:
        todos[todo_id]["title"] = todo.title

    if todo.status is not None:
        todos[todo_id]["status"] = todo.status
        todos[todo_id]["completed"] = todo.status == "completed"
    elif todo.completed is not None:
        todos[todo_id]["completed"] = todo.completed
        todos[todo_id]["status"] = "completed" if todo.completed else "pending"

    return todos[todo_id]


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    deleted = todos.pop(todo_id)
    return {"message": "Todo deleted", "todo": deleted}
