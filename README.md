# fastapi-todo

A simple Todo API built with FastAPI and persistent task storage using SQLite and SQLAlchemy.

## Features

- Create, read, update, and delete todo items.
- Filter todos by completion status (`GET /todos?is_done=true/false`).
- Automatic interactive API documentation with Swagger UI.
- Persistent storage with SQLite.
- Automated API tests with an isolated test database.
- Lightweight setup for local development.

## Tech Stack

- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pytest

## Project Structure

```bash
fastapi-todo/
├── main.py
├── requirements.txt
├── README.md
├── test_main.py
└── .gitignore
```

## Getting Started

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

## Running the application

Start the development server with:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Database

This project uses SQLite as the main database backend.

By default, the database file is created in the project root:

```python
sqlite:///./todo.db
```

If the database or tables do not exist yet, they are created automatically when the application starts.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health-check style root endpoint |
| GET | `/todos` | Return all todo items, optionally filtered by `is_done` |
| GET | `/todos/{id}` | Return a single todo item by ID |
| POST | `/todos` | Create a new todo item |
| PUT | `/todos/{id}` | Update an existing todo item |
| DELETE | `/todos/{id}` | Delete a todo item |

### Query parameters

- `GET /todos?is_done=true` — returns only completed todos.
- `GET /todos?is_done=false` — returns only pending todos.
- `GET /todos` — without `is_done` returns all todos.[web:828][web:831]

## Data validation

Request body for creating and updating todos is validated using Pydantic and FastAPI:

- `title` is required, 1–100 characters.
- `description` is optional, up to 300 characters.
- `is_done` is a boolean.
- `due_date` is an optional date in `YYYY-MM-DD` format.[web:826][web:835]

Invalid data returns a `422 Unprocessable Entity` response with details.[web:814]

## Running tests

Run tests with:

```powershell
.\venv\Scripts\python.exe -m pytest
```

The test suite uses a separate in-memory SQLite database with FastAPI dependency overrides, so tests do not write into the main `todo.db` file.[web:767][web:618]

## Example workflow

1. Start the server.
2. Open `http://127.0.0.1:8000/docs`.
3. Create a todo item with `POST /todos`.
4. Verify it appears in `GET /todos`.
5. Mark it as completed via `PUT /todos/{id}`.
6. Verify filters with `GET /todos?is_done=true` and `GET /todos?is_done=false`.

## Git workflow

This project follows a feature-branch workflow.

Example:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/todo-validation-filter
```

After implementation and testing:

```bash
git add main.py test_main.py README.md
git commit -m "feat: add todo validation and status filter"
git push -u origin feature/todo-validation-filter
```

Then open a Pull Request from `feature/todo-validation-filter` into `develop`.

## Notes

- Make sure dependencies are installed inside the local virtual environment.
- Avoid generating `requirements.txt` from a global Python installation.
- The main application uses `todo.db`, while tests use a separate in-memory SQLite database.