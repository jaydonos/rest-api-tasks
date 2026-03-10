# REST Task API (Flask + SQLite)

A lightweight REST API for managing tasks, built with Python and Flask.  
This project demonstrates practical backend engineering fundamentals: route design, input validation, structured error handling, persistence with SQLite, and clean data modeling with dataclasses.

## What This Project Does

- Creates tasks with text, tags, and due dates
- Retrieves a single task or all tasks
- Updates and deletes tasks by ID
- Filters tasks by tag
- Filters tasks by due date (`year/month/day`)

Each task is represented as:
- `id` (integer)
- `text` (string)
- `tags` (list of strings)
- `due` (ISO-8601 datetime string)

## Technical Highlights

- **Flask REST API** using method-specific route decorators (`@app.post`, `@app.get`, `@app.put`, `@app.delete`)
- **Dataclass domain model** (`Task`) with serialization via `to_dict()`
- **Custom API exception hierarchy** (`ApiError`, `BadRequestError`, `NotFoundError`) for consistent JSON error responses
- **SQLite persistence** with schema initialization at app startup
- **Manual JSON serialization/deserialization** for list fields (`tags`) using `json.dumps` / `json.loads`
- **Input validation** for request payload shape and datetime parsing

## Project Structure

```text
python-rest-tasks/
├── app.py         # Flask app, routes, validation, global error handlers
├── taskstore.py   # Data access layer and row-to-domain mapping
├── errors.py      # Custom API exception classes
├── db.py          # SQLite connection + schema bootstrap
├── schema.sql     # Database schema
└── requirements.txt
```

## API Endpoints

- `POST /tasks`  
  Create a task.
- `GET /task/`  
  Get all tasks.
- `GET /task/<task_id>/`  
  Get one task by ID.
- `PUT /task/<task_id>/`  
  Update a task by ID.
- `DELETE /task/<task_id>/`  
  Delete a task by ID.
- `GET /tag/<tag>/`  
  Get tasks containing a given tag.
- `GET /due/<year>/<month>/<day>/`  
  Get tasks due on a specific date.

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
python app.py
```

Server runs on `http://127.0.0.1:5000`.

## Example Request

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"text":"Finish project write-up","tags":["portfolio","backend"],"due":"2026-03-10T18:00:00"}'
```

## Why This Project Is Relevant

This codebase shows the ability to:
- Design and implement a complete CRUD API
- Separate HTTP layer, data access, and error concerns cleanly
- Work with structured data conversion between Python objects, JSON, and SQL storage
- Build maintainable backend code with clear, testable boundaries

