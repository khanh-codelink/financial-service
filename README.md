# Financial Service

Async FastAPI service backed by SQLite and SQLAlchemy, with Alembic migrations.

## Requirements

- Python 3.13+
- uv 0.12+

## Setup

Install dependencies:

```bash
uv sync
```

## Run database migrations

Use uv run (recommended for this project):

```bash
uv run alembic upgrade head
```

Notes:

- Do not use uvx here. On this machine, uvx is not available.
- If you need the equivalent behavior, use:

```bash
uv tool run alembic upgrade head
```

## Run the API

Start local dev server:

```bash
uv run fastapi dev src/financial_service/main.py
```

The app will be available at http://127.0.0.1:8000.

## Quick health check

```bash
curl http://127.0.0.1:8000/ping
```

Expected response:

```json
{"message":"pong"}
```

## View data in SQLite

The database URL is sqlite+aiosqlite:///./test.db, so the file is test.db in project root.

Open SQLite shell:

```bash
sqlite3 test.db
```

Useful queries:

```sql
.tables
.headers on
.mode column
SELECT * FROM user;
```

One-shot query from terminal:

```bash
sqlite3 -header -column test.db "SELECT * FROM user;"
```
