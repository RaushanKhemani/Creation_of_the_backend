# AI Hub Backend - Beginner Guide

## What is this?
This is the backend (the hidden working part) of your app.

If frontend is what users see, backend is what actually does the work behind the scenes.

---

## What this backend does in simple words
- Creates user accounts
- Logs users in
- Gives secure login tokens
- Saves API key details safely
- Detects which AI provider a key belongs to
- Lets users create chat windows
- Sends prompts and returns responses
- Saves chat history
- Tracks usage data like latency/tokens/cost

---

## Words you will see often
- **API**: a way apps communicate
- **Endpoint**: a URL where backend accepts requests
- **Token**: temporary login pass after successful login
- **Database**: storage for users/chats/messages
- **Rate limit**: prevents too many requests in short time

---

## How to run backend
Open PowerShell:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open in browser:
- `http://127.0.0.1:8000/docs`

This is Swagger UI (interactive API page).

---

## Quick health check
In another PowerShell window:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
.\smoke_check.ps1
```

---

## Full test check
```powershell
python -m pytest -q
```

---

## Basic flow to test in Swagger
1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login`
3. `POST /api/v1/integrations/api-key`
4. `POST /api/v1/chat/windows`
5. `POST /api/v1/chat/route`
6. `GET /api/v1/chat/conversations/{chat_id}/messages`

---

## Folder meaning (easy)
- `api/` -> endpoint files
- `services/` -> app logic
- `providers/` -> AI provider handling
- `db/` -> database tables/setup
- `schemas/` -> request/response structures
- `tests/` -> automatic checks

---

## Security reminder
- Never share real API keys
- Never commit secret files
- If key is leaked, rotate it immediately

---

## One-line summary
This backend is the brain and storage layer of your AI app.

---

## What important files do
- `app.py` -> starts your backend server.
- `config.py` -> keeps app settings (database URL, token time, limits, etc.).
- `requirements.txt` -> list of Python packages your backend needs.
- `smoke_check.ps1` -> quick script to check if backend is working.
- `README.md` -> technical project documentation.
- `README_BEGINNER.md` -> simple explanation for non-technical users.

### API layer
- `api/router.py` -> main API map that connects all route files.
- `api/dependencies.py` -> common helpers (login check, role check, rate limit).
- `api/routes/auth.py` -> register/login/refresh/logout/me endpoints.
- `api/routes/integrations.py` -> API key register + active integration endpoints.
- `api/routes/chat.py` -> chat window create/list + send message + history endpoints.
- `api/routes/providers.py` -> list/add providers.
- `api/routes/health.py` -> health and readiness endpoints.

### Service layer
- `services/auth_service.py` -> token creation, token refresh, password validation.
- `services/integration_service.py` -> detects provider from API key and stores key data.
- `services/chat_service.py` -> main chat logic, retry, timeout, usage log, cost tracking.
- `services/provider_service.py` -> provider list and default provider setup.
- `services/provider_gateway.py` -> sends prompt to provider abstraction.
- `services/crypto_service.py` -> encrypt/decrypt API keys.

### Provider layer
- `providers/base.py` -> standard format for provider responses.
- `providers/registry.py` -> picks which provider client to use.
- `providers/mock_provider.py` -> simulated AI provider response for now.

### Database layer
- `db/base.py` -> base class for all database tables.
- `db/session.py` -> database connection/session setup.
- `db/init_db.py` -> creates tables and seeds provider data.
- `db/models/user.py` -> user accounts table.
- `db/models/user_api_key.py` -> encrypted user API keys table.
- `db/models/conversation.py` -> chat window table (`chats`).
- `db/models/message.py` -> message history table.
- `db/models/usage_log.py` -> request logs (latency/tokens/cost/errors).
- `db/models/refresh_token.py` -> refresh token storage table.
- `db/models/provider.py` -> available providers table.

### Schema layer
- `schemas/auth.py` -> request/response format for auth.
- `schemas/integration.py` -> request/response format for integration API key flow.
- `schemas/chat.py` -> request/response format for chat and history.
- `schemas/provider.py` -> request/response format for providers.
- `schemas/user.py` -> user response format.
- `schemas/common.py` -> unified response envelope format.

### Core layer
- `core/app_factory.py` -> builds FastAPI app and startup logic.
- `core/security.py` -> bcrypt password hash/check + JWT helpers.
- `core/exceptions.py` -> centralized error responses.
- `core/logging.py` -> structured JSON logging setup.

### Migrations and deployment
- `alembic.ini` + `alembic/` -> database migration system.
- `Dockerfile` -> run backend in Docker container.
- `tests/` -> automated test files.
