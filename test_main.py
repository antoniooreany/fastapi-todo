from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def setup_function(function):
    main.todos.clear()
    main.todos.append(
        {
            "id": 1,
            "title": "Learn FastAPI basics",
            "description": "Create first endpoints and models",
            "is_done": False,
            "due_date": None,
        }
    )


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_get_todos():
    response = client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Learn FastAPI basics"


def test_get_todo_by_id():
    response = client.get("/todos/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI basics"


def test_get_todo_not_found():
    response = client.get("/todos/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo():
    response = client.post(
        "/todos",
        json={
            "title": "Learn testing",
            "description": "Write pytest tests",
            "is_done": False,
            "due_date": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["title"] == "Learn testing"
    assert data["description"] == "Write pytest tests"
    assert data["is_done"] is False
    assert data["due_date"] is None


def test_update_todo():
    response = client.put(
        "/todos/1",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "is_done": True,
            "due_date": "2026-07-20",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"
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
    response = client.delete("/todos/1")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Todo deleted"
    assert data["todo"]["id"] == 1

    follow_up = client.get("/todos/1")
    assert follow_up.status_code == 404


def test_delete_todo_not_found():
    response = client.delete("/todos/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}