import pytest
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def create_sample_todo(
    title="Test todo",
    description="Test description",
    is_done=False,
    due_date=None,
):
    payload = {
        "title": title,
        "description": description,
        "is_done": is_done,
        "due_date": due_date,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    return response.json()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_create_todo():
    payload = {
        "title": "Learn FastAPI",
        "description": "Build CRUD API",
        "is_done": False,
        "due_date": None,
    }

    response = client.post("/todos", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_done"] == payload["is_done"]
    assert data["due_date"] == payload["due_date"]


def test_get_todos_without_filter():
    created = create_sample_todo(
        title="Learn FastAPI",
        description="Build CRUD API",
        is_done=False,
        due_date=None,
    )

    response = client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == created["id"]


def test_get_todos_with_is_done_filter():
    create_sample_todo(
        title="Done task",
        description="Completed",
        is_done=True,
        due_date=None,
    )
    create_sample_todo(
        title="Pending task",
        description="Not completed yet",
        is_done=False,
        due_date=None,
    )

    response_done = client.get("/todos?is_done=true")
    response_pending = client.get("/todos?is_done=false")

    assert response_done.status_code == 200
    assert response_pending.status_code == 200

    data_done = response_done.json()
    data_pending = response_pending.json()

    assert all(todo["is_done"] is True for todo in data_done)
    assert all(todo["is_done"] is False for todo in data_pending)


def test_get_todo_by_id():
    created = create_sample_todo(
        title="Learn FastAPI",
        description="Build CRUD API",
        is_done=False,
        due_date=None,
    )

    response = client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build CRUD API"
    assert data["is_done"] is False
    assert data["due_date"] is None


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo():
    created = create_sample_todo(
        title="Old title",
        description="Old description",
        is_done=False,
        due_date=None,
    )

    response = client.put(
        f"/todos/{created['id']}",
        json={
            "title": "New title",
            "description": "New description",
            "is_done": True,
            "due_date": "2026-07-20",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "New title"
    assert data["description"] == "New description"
    assert data["is_done"] is True
    assert data["due_date"] == "2026-07-20"


def test_update_todo_not_found():
    response = client.put(
        "/todos/999",
        json={
            "title": "Missing",
            "description": "Missing",
            "is_done": False,
            "due_date": None,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo():
    created = create_sample_todo(
        title="Delete me",
        description="Temporary task",
        is_done=False,
        due_date=None,
    )

    response = client.delete(f"/todos/{created['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Todo deleted"
    assert data["todo"]["id"] == created["id"]


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_validation_title_required():
    payload = {
        "description": "Missing title",
        "is_done": False,
        "due_date": None,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 422


def test_validation_description_max_length():
    long_description = "x" * 400
    payload = {
        "title": "Too long description",
        "description": long_description,
        "is_done": False,
        "due_date": None,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 422


def test_validation_due_date_format():
    payload = {
        "title": "Bad date format",
        "description": "Invalid due date",
        "is_done": False,
        "due_date": "20-07-2026",
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 422