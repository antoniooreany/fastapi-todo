from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_get_todos_returns_list():
    response = client.get("/todos")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "title" in data[0]
    assert "is_done" in data[0]


def test_create_todo():
    payload = {
        "title": "Write tests",
        "description": "Create first API tests",
        "is_done": False,
        "due_date": None
    }

    response = client.post("/todos", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] >= 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_done"] == payload["is_done"]
    assert data["due_date"] == payload["due_date"]