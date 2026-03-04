# AI Hub Backend (Production-Ready Architecture)

## Layers
- `api/` - route layer and dependencies
- `services/` - business logic
- `providers/` - provider abstraction and async clients
- `db/` - SQLAlchemy models, session, init
- `schemas/` - request/response schemas
- `core/` - app factory, logging, security, exceptions

## Features
- JWT auth with access + refresh tokens
- bcrypt password hashing
- Encrypted user API key storage (Fernet)
- Role-based access control
- Per-user rate limiting
- Centralized error handling
- Structured logging
- Usage logging with cost/tokens/latency
- Async AI provider calls with timeout + retry
- Chat windows + message history
- Env-based config
- Alembic migration scaffold
- Dockerfile

## Run
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

## Swagger
- http://127.0.0.1:8000/docs

## Tests
```powershell
python -m pytest -q
.\smoke_check.ps1
```

## Migrations
```powershell
alembic upgrade head
```
