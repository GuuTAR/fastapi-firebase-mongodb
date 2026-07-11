# fastapi-firebase-mongodb

Reusable project template: FastAPI + Firebase Authentication + MongoDB (via Beanie).

## Stack

- **FastAPI** for the HTTP API
- **Beanie** (async ODM on top of PyMongo's native async client) for MongoDB
- **firebase-admin** to verify Firebase ID tokens and protect routes
- **uv** for dependency management

## Project Structure

```
app/
  core/
    config.py    # settings (env vars via pydantic-settings)
    db.py        # MongoDB connection + Beanie init
    security.py  # Firebase ID token verification, CurrentUser dependency
  models/        # Beanie documents
  schemas/       # Pydantic response/request models
  api/
    routes/      # route modules
    router.py    # aggregates routers
  main.py        # FastAPI app + lifespan
```

## Setup

1. Copy `.env.example` to `.env` and fill in
2. Running server

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8080
```
