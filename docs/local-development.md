# Local development

This document describes the provided application before Docker Compose is introduced.

## Prerequisites

- Python 3 with `venv`
- PostgreSQL running locally
- Node.js and npm

Redis is optional. When `REDIS_HOST` is not set, the backend runs without cache support.

## Backend

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
export DATABASE_URL="postgresql://taskflow:taskflow_dev_password@localhost:5432/tasks"
cd backend
python -m uvicorn Back.main:app --host 0.0.0.0 --port 8000
```

Check the service in another terminal:

```bash
curl http://localhost:8000/health
```

## Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server proxies `/api` requests to the backend. Its default target is `http://localhost:8000`.
