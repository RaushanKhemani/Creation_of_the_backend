# AI Hub Backend

Production-oriented FastAPI backend for an AI Hub where users can chat and switch across providers (OpenAI/ChatGPT, Gemini, Claude, Grok, Groq).

## What This Backend Provides
- Auth system with JWT access + refresh tokens
- Role-based access control and per-user rate limiting
- Secure API key handling (encrypted at rest with Fernet)
- Provider routing layer with async calls, timeout, and retry
- Chat windows, persistent message history, and usage logs
- Cost/tokens/latency tracking per request
- Swagger API docs and a simple local Chat UI

## Architecture
- `api/` -> HTTP routes and dependencies
- `services/` -> business logic
- `providers/` -> provider clients and provider registry
- `db/` -> SQLAlchemy models, session, and init
- `schemas/` -> request/response contracts
- `core/` -> app factory, logging, security, exceptions

## Supported Providers (Current)
- `chatgpt` (OpenAI API)
- `gemini` (Google Gemini API)
- `claude` (Anthropic API)
- `grok` (xAI API)
- `groq` (Groq API)

Note: `copilot` exists in provider metadata but is not implemented as a direct runtime client in this backend flow.

## Quick Start
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## Local Interfaces
- Swagger docs: `http://127.0.0.1:8000/docs`
- Chat UI: `http://127.0.0.1:8000/chat-ui`

## Environment Setup
Copy `.env.example` to `.env` and configure:

Required core:
- `JWT_SECRET_KEY`
- `API_KEY_ENCRYPTION_KEY`
- `DATABASE_URL`

Provider keys (platform-managed mode):
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- `XAI_API_KEY`
- `GROQ_API_KEY`

Optional provider model overrides:
- `OPENAI_MODEL`
- `GEMINI_MODEL`
- `ANTHROPIC_MODEL`
- `XAI_MODEL`
- `GROQ_MODEL`

## Chat Modes
1. Platform-managed (recommended): configure provider keys in `.env`; users chat without entering raw provider keys.
2. BYOK (optional): users can register their own key via `/api/v1/integrations/api-key`.

## Basic API Flow
1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login`
3. `POST /api/v1/chat/route` (platform-key mode), or
4. `POST /api/v1/integrations/api-key` then `POST /api/v1/chat/route` (BYOK mode)
5. `GET /api/v1/chat/conversations/{chat_id}/messages`

## Testing
Quick smoke check:
```powershell
.\smoke_check.ps1
```

Automated tests:
```powershell
python -m pytest -q
```

## Database Migration
```powershell
alembic upgrade head
```

If schema changed and local SQLite is stale, recreate local DB before rerun:
```powershell
Remove-Item .\ai_hub.db -Force
python -m uvicorn app:app --reload
```

## Docker
```powershell
docker build -t ai-hub-backend .
docker run --rm -p 8000:8000 ai-hub-backend
```
