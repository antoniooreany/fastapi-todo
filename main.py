from datetime import date

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Session


app = FastAPI()

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    is_done = Column(Boolean, default=False, index=True)
    due_date = Column(Date, nullable=True)


Base.metadata.create_all(bind=engine)


class TodoBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Short title for the todo item (1-100 characters).",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=300,
        description="Optional description (up to 300 characters).",
    )
    is_done: bool = Field(
        default=False,
        description="Completion status of the todo item.",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date for the todo item (YYYY-MM-DD).",
    )


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.get("/todos", response_model=list[TodoRead])
def get_todos(
    is_done: Optional[bool] = Query(
        default=None,
        description="Optional filter by completion status. If omitted, returns all todos.",
    ),
    db: Session = Depends(get_db),
):
    query = db.query(TodoDB)

    if is_done is not None:
        query = query.filter(TodoDB.is_done == is_done)

    todos = query.all()
    return todos


@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoRead, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodoDB(
        title=todo.title,
        description=todo.description,
        is_done=todo.is_done,
        due_date=todo.due_date,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.is_done = updated_todo.is_done
    todo.due_date = updated_todo.due_date

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted", "todo": {"id": todo_id}}