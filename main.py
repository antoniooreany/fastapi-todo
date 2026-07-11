from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[str] = None


class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[str] = None


todos = [
    {
        "id": 1,
        "title": "Learn FastAPI basics",
        "description": "Create first endpoints and models",
        "is_done": False,
        "due_date": None,
    }
]


@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.get("/todos", response_model=list[TodoRead])
def get_todos():
    return todos


@app.post("/todos", response_model=TodoRead)
def create_todo(todo: TodoCreate):
    new_id = len(todos) + 1

    new_todo = {
        "id": new_id,
        "title": todo.title,
        "description": todo.description,
        "is_done": todo.is_done,
        "due_date": todo.due_date,
    }

    todos.append(new_todo)
    return new_todo