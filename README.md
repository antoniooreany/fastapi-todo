# FastAPI Todo API

A simple Todo API built with FastAPI and SQLite.

This project provides a small REST API for managing todo items.  
It supports creating, reading, updating, deleting, filtering, and validating todos.

## Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic
- SQLAlchemy
- Pytest

## Features

- Create, read, update, and delete todo items
- Filter todos by status with `is_done=true/false`
- Validate request data with Pydantic
- Interactive API docs with Swagger UI
- SQLite database for persistent storage
- Automated tests with Pytest

## Project Structure

```bash
fastapi-todo/
├── main.py
├── test_main.py
├── requirements.txt
├── README.md
└── todo.db
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-todo
```

### 2. Create and activate a virtual environment

#### PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the server

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

FastAPI automatically generates interactive API documentation at `/docs`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/todos` | Get all todos |
| GET | `/todos/{id}` | Get a todo by ID |
| POST | `/todos` | Create a todo |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

## Query Parameters

`GET /todos` supports an optional query parameter:

- `is_done=true` — return only completed todos
- `is_done=false` — return only pending todos

## Request Validation

Todo items are validated with Pydantic:

- `title` is required
- `title` max length: 100 characters
- `description` max length: 300 characters
- `due_date` must be in `YYYY-MM-DD` format

Invalid input returns `422 Unprocessable Entity`.

## Example Requests

### Create a todo

```bash
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn FastAPI\",\"description\":\"Build a Todo API\",\"is_done\":false,\"due_date\":null}"
```

### Get all todos

```bash
curl "http://127.0.0.1:8000/todos"
```

### Get completed todos

```bash
curl "http://127.0.0.1:8000/todos?is_done=true"
```

### Get pending todos

```bash
curl "http://127.0.0.1:8000/todos?is_done=false"
```

### Update a todo

```bash
curl -X PUT "http://127.0.0.1:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn FastAPI\",\"description\":\"Updated task\",\"is_done\":true,\"due_date\":\"2026-07-20\"}"
```

### Delete a todo

```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1"
```

## Run tests

```powershell
.\venv\Scripts\python.exe -m pytest
```

## Notes

- If you change the SQLite schema during development, you may need to delete `todo.db` and let the app recreate it.
- Test cases use a separate in-memory SQLite database.
- This project is intended as a beginner-friendly backend portfolio project.