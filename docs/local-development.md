# Local development

This guide runs the provided application directly on Ubuntu before Docker Compose is introduced.

## Prerequisites

- Python 3 with `venv`
- PostgreSQL running locally
- Node.js and npm for the frontend

Redis is optional. When `REDIS_HOST` is not set, the backend runs without cache support.

## PostgreSQL setup

Install PostgreSQL and start its service:

```bash
sudo apt update
sudo apt install -y postgresql
sudo systemctl enable --now postgresql
```

Create a development-only database user and database:

```bash
sudo -u postgres psql -c "CREATE USER taskflow WITH PASSWORD 'taskflow_dev_password';"
sudo -u postgres psql -c "CREATE DATABASE tasks OWNER taskflow;"
```

## Python virtual environment

From the repository root, create and activate the project-local environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

On Ubuntu, do not install project dependencies with `sudo pip` or `--break-system-packages`.

## Backend startup

The backend is a Python package whose entry point is `backend/main.py`. Run it from the repository root so relative imports resolve correctly:

```bash
export DATABASE_URL="postgresql://taskflow:taskflow_dev_password@localhost:5432/tasks"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Backend lint and tests

Run these commands from the repository root. They are the same checks used by
the CI test job and do not require PostgreSQL or Redis:

```bash
python -m pip install --no-cache-dir ruff pytest httpx
ruff check backend
python -m pytest backend/tests
```

If Ruff reports fixable formatting or import errors, apply only its safe
automatic fixes, review the change, then run the checks again:

```bash
ruff check backend --fix
git diff
ruff check backend
python -m pytest backend/tests
```

Do this locally and commit the resulting source changes. The CI pipeline should
report lint errors, not silently fix them in its temporary job workspace.

## Verification

In another terminal:

```bash
curl http://localhost:8000/health
```

| Address | Expected result |
| --- | --- |
| `/` | `404` is normal; the backend does not define a root route. |
| `/health` | API health response. |
| `/docs` | Swagger UI for testing the REST API. |
| `/tasks/` | Task REST API response. |

When creating a first task, omit `owner_id` or set it to `null` unless that user record already exists.

## Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server proxies `/api` requests to the backend. Its default target is `http://localhost:8000`.

## Common errors

| Error | Cause | Fix |
| --- | --- | --- |
| `externally-managed-environment` | Project packages were installed into Ubuntu's system Python. | Create and activate `.venv`, then use `python -m pip`. |
| `No module named Back` | An old command assumes a `backend/Back/` directory. | Run `python -m uvicorn backend.main:app` from the repository root. |
| `attempted relative import with no known parent package` | `main.py` was run as a standalone module. | Run `backend.main:app`, not `main:app`. |
| `422 User 1 does not exist` | A task refers to an owner that is not in the database. | Omit `owner_id`, use `null`, or create the referenced user first. |
