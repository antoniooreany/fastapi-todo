from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def setup_function(function):
    main.todos.clear()
    main.next_id = 1


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_create_todo():
    response = client.post(
        "/todos",
        json={
            "title": "Learn FastAPI",
            "description": "Build CRUD API",
            "is_done": False,
            "due_date": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build CRUD API"
    assert data["is_done"] is False
    assert data["due_date"] is None


def test_get_todos():
    client.post(
        "/todos",
        json={
            "title": "Learn FastAPI",
            "description": "Build CRUD API",
            "is_done": False,
            "due_date": None,
        },
    )

    response = client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_todo_by_id():
    created = client.post(
        "/todos",
        json={
            "title": "Learn FastAPI",
            "description": "Build CRUD API",
            "is_done": False,
            "due_date": None,
        },
    ).json()

    response = client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "Learn FastAPI"


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo():
    created = client.post(
        "/todos",
        json={
            "title": "Old title",
            "description": "Old description",
            "is_done": False,
            "due_date": None,
        },
    ).json()

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
    created = client.post(
        "/todos",
        json={
            "title": "Delete me",
            "description": "Temporary task",
            "is_done": False,
            "due_date": None,
        },
    ).json()

    response = client.delete(f"/todos/{created['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Todo deleted"
    assert data["todo"]["id"] == created["id"]


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}