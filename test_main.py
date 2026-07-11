from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_sample_todo(
    title="Test todo",
    description="Test description",
    is_done=False,
):
    payload = {
        "title": title,
        "description": description,
        "is_done": is_done,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_todo():
    payload = {
        "title": "Learn FastAPI",
        "description": "Read docs and build API",
        "is_done": False,
    }

    response = client.post("/todos", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_done"] == payload["is_done"]
    assert "id" in data


def test_list_todos():
    created = create_sample_todo(title="List todo")

    response = client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(todo["id"] == created["id"] for todo in data)


def test_get_todo_by_id():
    created = create_sample_todo(title="Get todo")

    response = client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "Get todo"


def test_update_todo():
    created = create_sample_todo(title="Old title")

    update_payload = {
        "title": "New title",
        "description": "Updated description",
        "is_done": True,
    }

    response = client.put(f"/todos/{created['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == update_payload["title"]
    assert data["description"] == update_payload["description"]
    assert data["is_done"] is True


def test_delete_todo():
    created = create_sample_todo(title="Delete todo")

    delete_response = client.delete(f"/todos/{created['id']}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/todos/{created['id']}")
    assert get_response.status_code == 404


def test_get_missing_todo():
    response = client.get("/todos/999999")
    assert response.status_code == 404