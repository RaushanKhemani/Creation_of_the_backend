# AI Hub Backend

Backend service for an AI hub app where users can switch between different AI providers.

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite (default local DB)
- JWT authentication
- Pytest

## Project Structure
- `app.py`: FastAPI entrypoint
- `config.py`: environment/config settings
- `api/`: route handlers and dependencies
- `core/`: app factory, security, exception handling
- `db/`: database engine/session/models/init
- `schemas/`: request/response models
- `services/`: business logic and provider/chat orchestration
- `tests/`: automated tests

## Setup
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
```

## Run Server
```powershell
uvicorn app:app --reload
```

Open Swagger docs:
- http://127.0.0.1:8000/docs

## Quick Health Check
```powershell
python -c "from fastapi.testclient import TestClient; from app import app; c=TestClient(app); r=c.get('/api/v1/health'); print(r.status_code, r.json().get('status'))"
```
Expected output: `200 ok`

## Smoke Check Script
```powershell
.\smoke_check.ps1
```

## Run Tests
```powershell
python -m pytest -q
```

## Main API Endpoints
- `GET /api/v1/health`
- `GET /api/v1/health/ready`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/token` (Swagger OAuth form)
- `GET /api/v1/auth/me`
- `GET /api/v1/providers`
- `GET /api/v1/providers/{provider_key}`
- `POST /api/v1/providers` (superuser)
- `POST /api/v1/chat/route`
- `GET /api/v1/chat/conversations/{conversation_id}/messages`

## Default Local DB
- Uses SQLite by default
- File: `ai_hub.db`
- Tables are auto-created on startup

## Notes
- `services/provider_gateway.py` currently returns simulated provider responses.
- This design is ready for plugging in real provider APIs next..
