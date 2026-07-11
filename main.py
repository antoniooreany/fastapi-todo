from fastapi import FastAPI, HTTPException
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


@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


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


@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, updated_todo: TodoCreate):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = updated_todo.title
            todo["description"] = updated_todo.description
            todo["is_done"] = updated_todo.is_done
            todo["due_date"] = updated_todo.due_date
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(index)
            return {"message": "Todo deleted", "todo": deleted_todo}
    raise HTTPException(status_code=404, detail="Todo not found")