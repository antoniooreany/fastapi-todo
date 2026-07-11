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

todos = []

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/todos", response_model=list[TodoRead])
def get_todos():
    return todos