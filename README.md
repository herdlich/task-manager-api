# Task Manager API

A REST API for managing tasks, built with FastAPI, Pydantic, SQLite, and pytest.

The project demonstrates a complete CRUD workflow:

```text
HTTP request
→ FastAPI endpoint
→ Pydantic validation
→ SQLite database operation
→ response model validation
→ JSON response
```

## Features

- Create tasks
- Read all tasks
- Read a task by ID
- Partially update tasks
- Delete tasks
- Persistent SQLite storage
- Request and response validation with Pydantic
- Automatic interactive API documentation
- Isolated tests using temporary databases

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- pytest
- FastAPI TestClient

## Project Structure

```text
task-manager-api/
├── data/
│   └── tasks.db
├── src/
│   └── task_manager_api/
│       ├── __init__.py
│       ├── api.py
│       ├── database.py
│       └── models.py
├── tests/
│   ├── conftest.py
│   ├── test_api_post.py
│   ├── test_api_get.py
│   ├── test_api_patch.py
│   ├── test_api_delete.py
│   └── test_database.py
├── pyproject.toml
├── README.md
├── .gitignore
└── requirements.txt
```

## Data Model

A task contains the following fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | integer | generated | Unique identifier created by SQLite |
| `title` | string | yes | Non-empty task title |
| `description` | string or null | no | Optional task description |
| `due_date` | date or null | no | Optional due date in `YYYY-MM-DD` format |

Example:

```json
{
  "id": 1,
  "title": "List of products",
  "description": "Milk, eggs, bread",
  "due_date": "2026-07-12"
}
```

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/herdlich/task-manager-api.git
cd task-manager-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux and macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project and its dependencies declared in `pyproject.toml`:

```bash
pip install -e .
```

## Running the API

Run Uvicorn from the project root:

```bash
uvicorn task_manager_api.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

| Method | Endpoint | Description | Success status |
|---|---|---|---:|
| `GET` | `/health` | Check API availability | `200` |
| `POST` | `/tasks` | Create a task | `201` |
| `GET` | `/tasks` | Return all tasks | `200` |
| `GET` | `/tasks/{task_id}` | Return one task | `200` |
| `PATCH` | `/tasks/{task_id}` | Partially update a task | `200` |
| `DELETE` | `/tasks/{task_id}` | Delete and return a task | `200` |

A request for a missing task returns:

```json
{
  "detail": "No task found"
}
```

with status code `404`.

Invalid request data returns status code `422`.

## Usage Examples

### Create a task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "List of products",
    "description": "Milk, eggs, bread",
    "due_date": "2026-07-12"
  }'
```

Response:

```json
{
  "id": 1,
  "title": "List of products",
  "description": "Milk, eggs, bread",
  "due_date": "2026-07-12"
}
```

### Get all tasks

```bash
curl "http://127.0.0.1:8000/tasks"
```

### Get one task

```bash
curl "http://127.0.0.1:8000/tasks/1"
```

### Update a task

Only fields included in the request are changed:

```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated product list"
  }'
```

An empty JSON object is accepted and leaves the task unchanged:

```json
{}
```

The `title` field may be omitted during an update, but explicitly sending `"title": null` is rejected.

### Delete a task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

The endpoint returns the deleted task.

## Validation Rules

- `title` is required when creating a task.
- Leading and trailing whitespace is removed from `title`.
- An empty or whitespace-only title is rejected.
- `due_date` must use the ISO format `YYYY-MM-DD`.
- `description` and `due_date` may be `null`.
- During partial updates, omitted fields remain unchanged.
- During partial updates, `title: null` is rejected.

## Database

The application uses SQLite.

The database file is stored at:

```text
data/tasks.db
```

SQLite generates task IDs automatically. Dates are stored as ISO-formatted text, and optional values are stored as SQL `NULL`.

The database layer is separated from the HTTP layer:

- `api.py` handles requests, responses, and HTTP errors.
- `database.py` contains SQL and database operations.
- `models.py` contains request and response models.

## Tests

Run the complete test suite:

```bash
pytest -q
```

The tests cover:

- successful CRUD operations
- missing-task `404` responses
- request validation
- empty and whitespace-only titles
- invalid dates
- `title: null` during updates
- empty partial updates
- SQLite inserts and reads
- nullable dates
- empty task lists
- reading multiple tasks
- response data integrity

API tests use an isolated SQLite database created inside pytest's `tmp_path`. The application database is not modified during tests.

## Current Scope

This project intentionally uses direct SQLite queries to demonstrate the complete request-to-database flow without hiding it behind an ORM.

Potential future improvements include:

- task completion status
- filtering and pagination
- SQLAlchemy
- PostgreSQL
- database migrations
- Docker
- authentication
- structured logging
- deployment

## License

This project is intended for educational and portfolio use.