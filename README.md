# fastapi-todo

A simple Todo API built with FastAPI and persistent task storage using SQLite and SQLAlchemy.

## Features

- Create, read, update, and delete todo items.
- Automatic interactive API documentation with Swagger UI.
- Persistent storage with SQLite.
- Lightweight setup for local development.

## Tech Stack

- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Project Structure

```bash
fastapi-todo/
├── main.py
├── requirements.txt
├── README.md
├── test_main.py
├── todo.db
└── venv/
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

This project uses SQLite as the database backend.

By default, the database file is created in the project root:

```python
sqlite:///./todo.db
```

If the database or tables do not exist yet, they are created automatically when the application starts.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | Return all todo items |
| GET | `/todos/{id}` | Return a single todo item by ID |
| POST | `/todos` | Create a new todo item |
| PUT | `/todos/{id}` | Update an existing todo item |
| DELETE | `/todos/{id}` | Delete a todo item |

## Running tests

Run tests with:

```powershell
.\venv\Scripts\python.exe -m pytest
```

## Example workflow

1. Start the server.
2. Open `http://127.0.0.1:8000/docs`.
3. Create a todo item with `POST /todos`.
4. Verify it appears in `GET /todos`.
5. Restart the server and confirm the data is still stored.

## Git workflow

This feature is developed in a dedicated feature branch:

```bash
git checkout develop
git checkout -b feature/todo-database
```

After implementation and testing:

```bash
git add main.py test_main.py README.md requirements.txt
git commit -m "feat: persist todos with SQLite and SQLAlchemy"
git push -u origin feature/todo-database
```

Then open a Pull Request from `feature/todo-database` into `develop`.

## Notes

- Make sure dependencies are installed inside the local virtual environment.
- Avoid generating `requirements.txt` from a global Python installation.
- The `todo.db` file may be excluded from version control depending on project rules.