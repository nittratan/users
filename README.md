# In-memory User API

FastAPI CRUD API with random user IDs, validation, centralized error responses,
request IDs, request logging, timestamps, pagination, and thread-safe access.

## Project structure

```text
app/
├── api/routes/          # HTTP endpoints
├── core/                # Config, logging and exception handlers
├── middleware/          # Request logging and request IDs
├── repositories/        # In-memory data access
├── schemas/             # Pydantic request/response models
├── services/            # Business logic
├── dependencies.py      # Shared dependency wiring
└── main.py              # FastAPI app factory
tests/                   # API tests
main.py                  # Backward-compatible entrypoint
Dockerfile               # Non-root production container
compose.yaml             # Local container orchestration
pyproject.toml           # Package and tool configuration
```

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI at <http://127.0.0.1:8000/docs>.

The old `uvicorn main:app --reload` command also remains supported.

Common commands are also available through `make`:

```bash
make run
make test
make lint
```

## Test

```bash
pip install -r requirements-dev.txt
pytest
```

## Endpoints

- `POST /users` - create user
- `GET /users?offset=0&limit=100` - list users
- `GET /users/{user_id}` - get one user
- `PATCH /users/{user_id}` - update user
- `DELETE /users/{user_id}` - delete user
- `GET /health` - health check

Example request body:

```json
{
  "name": "Aman",
  "email": "aman@example.com",
  "age": 24
}
```

Data is stored in a Python list and is cleared whenever the server restarts.

Generated IDs look like `user482731`. Every response includes an `X-Request-ID`
header, and errors use one consistent JSON structure.

## Deployment note

Create local environment settings without committing secrets:

```bash
cp .env.example .env
```

Build and run the production-style container:

```bash
docker compose up --build
```

Or use Docker directly:

```bash
docker build -t user-api .
docker run --rm -p 8000:8000 --env-file .env user-api
```

The image runs as a non-root user and includes a `/health` health check. Run only
one worker while using in-memory storage:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

Multiple processes do not share a Python list. Replace the list with PostgreSQL
before deploying multiple workers or instances.
