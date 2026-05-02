---
name: rest-api-in-one-day
description: Define resources, write an OpenAPI 3.1 schema, scaffold FastAPI, and ship 4 working endpoints with validation and curl tests.
tier: solo
group: api-design
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a running FastAPI application that exposes four endpoints for a `Task` resource (`GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `DELETE /tasks/{id}`), backed by an OpenAPI 3.1 schema you wrote first, with Pydantic input validation and a passing curl test suite.

## Prerequisites

- Python 3.11+ installed (`python3 --version`).
- `pip` available (`pip --version`).
- Basic Python knowledge (functions, dicts, classes).
- A terminal and a text editor.
- No database required — storage is in-memory for this playbook.

## Steps

1. Create a project directory and a virtual environment:

   ```bash
   mkdir taskapi && cd taskapi
   python3 -m venv .venv
   source .venv/bin/activate
   pip install fastapi "uvicorn[standard]" pydantic
   ```

2. Define your resource on paper first. A `Task` has three fields:

   | Field | Type | Rules |
   |-------|------|-------|
   | `id` | integer | auto-assigned, read-only |
   | `title` | string | required, 1–200 chars |
   | `done` | boolean | default `false` |

3. Write the OpenAPI 3.1 schema to `openapi.yaml` before touching any code (contract-first):

   ```yaml
   openapi: "3.1.0"
   info:
     title: Task API
     version: "1.0.0"
   paths:
     /tasks:
       get:
         summary: List all tasks
         responses:
           "200":
             description: Array of tasks
             content:
               application/json:
                 schema:
                   type: array
                   items:
                     $ref: "#/components/schemas/Task"
       post:
         summary: Create a task
         requestBody:
           required: true
           content:
             application/json:
               schema:
                 $ref: "#/components/schemas/TaskCreate"
         responses:
           "201":
             description: Created task
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Task"
     /tasks/{id}:
       get:
         summary: Get one task
         parameters:
           - name: id
             in: path
             required: true
             schema:
               type: integer
         responses:
           "200":
             description: The task
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/Task"
           "404":
             description: Not found
       delete:
         summary: Delete a task
         parameters:
           - name: id
             in: path
             required: true
             schema:
               type: integer
         responses:
           "204":
             description: Deleted
           "404":
             description: Not found
   components:
     schemas:
       TaskCreate:
         type: object
         required: [title]
         properties:
           title:
             type: string
             minLength: 1
             maxLength: 200
           done:
             type: boolean
             default: false
       Task:
         allOf:
           - $ref: "#/components/schemas/TaskCreate"
           - type: object
             required: [id]
             properties:
               id:
                 type: integer
   ```

4. Create `main.py` that implements the four endpoints, following the schema:

   ```python
   from fastapi import FastAPI, HTTPException, status
   from pydantic import BaseModel, Field

   app = FastAPI(title="Task API", version="1.0.0")

   # --- Models ---

   class TaskCreate(BaseModel):
       title: str = Field(..., min_length=1, max_length=200)
       done: bool = False

   class Task(TaskCreate):
       id: int

   # --- In-memory store ---

   _tasks: dict[int, Task] = {}
   _next_id: int = 1

   # --- Endpoints ---

   @app.get("/tasks", response_model=list[Task])
   def list_tasks():
       return list(_tasks.values())

   @app.get("/tasks/{task_id}", response_model=Task)
   def get_task(task_id: int):
       task = _tasks.get(task_id)
       if task is None:
           raise HTTPException(status_code=404, detail="Task not found")
       return task

   @app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
   def create_task(payload: TaskCreate):
       global _next_id
       task = Task(id=_next_id, **payload.model_dump())
       _tasks[_next_id] = task
       _next_id += 1
       return task

   @app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
   def delete_task(task_id: int):
       if task_id not in _tasks:
           raise HTTPException(status_code=404, detail="Task not found")
       del _tasks[task_id]
   ```

5. Start the server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

   Leave this terminal open. Open a second terminal for the next step.

6. Run the four curl tests in order:

   ```bash
   # Create two tasks
   curl -s -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Buy groceries"}' | python3 -m json.tool

   curl -s -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Ship the MVP", "done": false}' | python3 -m json.tool

   # List all tasks
   curl -s http://localhost:8000/tasks | python3 -m json.tool

   # Get task 1
   curl -s http://localhost:8000/tasks/1 | python3 -m json.tool

   # Delete task 1
   curl -s -o /dev/null -w "%{http_code}" -X DELETE http://localhost:8000/tasks/1

   # Confirm deletion (expect 404)
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/tasks/1
   ```

7. Validate that your running server matches the schema you wrote in Step 3. FastAPI auto-generates OpenAPI at `/openapi.json`. Compare the `paths` keys:

   ```bash
   curl -s http://localhost:8000/openapi.json | python3 -c "
   import json, sys
   spec = json.load(sys.stdin)
   for path in spec['paths']:
       print(path, list(spec['paths'][path].keys()))
   "
   ```

   Expected output lists `/tasks` (get, post) and `/tasks/{task_id}` (get, delete).

## Verify

Run all four HTTP methods and check the status codes:

```bash
# Create (expect 201)
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify step"}'

# List (expect 200)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/tasks

# Get (expect 200 for id=2, which was created in Step 6)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/tasks/2

# Delete (expect 204)
curl -s -o /dev/null -w "%{http_code}" -X DELETE http://localhost:8000/tasks/2
```

All four lines print `201`, `200`, `200`, `204` in sequence. If any line returns `422`, check the request body JSON. If any line returns `500`, check the uvicorn terminal for a Python traceback.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl` returns `422 Unprocessable Entity` on POST | `title` field missing or exceeds 200 chars | Send `{"title": "something"}` with valid string; check `Content-Type: application/json` header is present |
| `uvicorn: command not found` after `pip install` | venv not activated | Run `source .venv/bin/activate` then retry |
| DELETE returns `200` instead of `204` | Wrong status code on the decorator | Add `status_code=status.HTTP_204_NO_CONTENT` to `@app.delete(...)` |
| POST returns `200` instead of `201` | Missing `status_code` on the decorator | Add `status_code=status.HTTP_201_CREATED` to `@app.post(...)` |
| `GET /tasks/99` returns `200` with `null` instead of `404` | `_tasks.get()` returns `None` and FastAPI serialises it | Add the `if task is None: raise HTTPException(...)` guard as shown in Step 4 |
| Server changes not reflected on save | `--reload` flag missing | Stop uvicorn, restart with `uvicorn main:app --reload --port 8000` |

## Next

- `api-key-auth` — add an `X-API-Key` header guard to every endpoint so only authorised callers can write or delete tasks.
- Persist tasks to SQLite using SQLModel (drop-in with FastAPI) to survive server restarts.
- `github-actions-cicd` — run `pytest` against these endpoints on every push to catch regressions automatically.

## References

- [knowledge/solo/dev/api-developer/api-rest-design](../../../knowledge/solo/dev/api-developer/api-rest-design) — grounds the resource-naming and HTTP method choices in Steps 2–4; the `Task` resource shape and status codes (201, 204, 404) map directly to the REST design principles in this methodology.
- [knowledge/solo/dev/api-developer/api-contract-first](../../../knowledge/solo/dev/api-developer/api-contract-first) — drives the "write OpenAPI before code" order in Steps 3–4; this playbook's schema-first sequence is the direct application of the contract-first practice.
- [knowledge/solo/dev/api-developer/api-openapi-spec](../../../knowledge/solo/dev/api-developer/api-openapi-spec) — provides the OpenAPI 3.1 component and path syntax used verbatim in the `openapi.yaml` written in Step 3.
