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

---

## Start Here (First Time Checklist)
1. Open PowerShell and go to project folder.
2. Install required packages.
3. Start backend server.
4. Open Swagger page (`/docs`).
5. Create account (`/auth/register`).
6. Login (`/auth/login`) and copy access token.
7. Click `Authorize` in Swagger and enter credentials if needed.
8. Add API key (`/integrations/api-key`).
9. Create chat window (`/chat/windows`).
10. Send chat prompt (`/chat/route`).
11. Check message history (`/chat/conversations/{chat_id}/messages`).
12. Run smoke check and tests before pushing code.

### Commands
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

In another PowerShell:
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
.\smoke_check.ps1
python -m pytest -q
```

---

## Start Here Checklist (Detailed, Non-Coder Version)

### Step 1: Open your project folder
What this means:
- You are telling PowerShell to go inside your backend folder.
- All next commands must run from this folder.

Command:
```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
```

How to confirm:
- Your PowerShell line should show the same path at the left side.

---

### Step 2: Install required software packages
What this means:
- Your backend needs helper libraries (FastAPI, SQLAlchemy, JWT, bcrypt, etc.).
- `requirements.txt` is the package list.

Command:
```powershell
pip install -r requirements.txt
```

How to confirm:
- Command finishes without red error lines.

---

### Step 3: Start backend server
What this means:
- This turns your backend ON.
- Keep this window open while testing.

Command:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

How to confirm:
- You should see `Uvicorn running on http://127.0.0.1:8000`.

---

### Step 4: Open Swagger UI (testing page)
What this means:
- Swagger is a built-in test page for your backend.
- You can click APIs and test without writing frontend code.

Open in browser:
- `http://127.0.0.1:8000/docs`

---

### Step 5: Create user account in Swagger
What this means:
- First you create a login account for your backend.

Where:
- `POST /api/v1/auth/register`

Sample body:
```json
{
  "email": "your_email@example.com",
  "password": "StrongPass123",
  "full_name": "Your Name"
}
```

---

### Step 6: Login and get access token
What this means:
- Login returns a temporary access token.
- This token proves "you are logged in".

Where:
- `POST /api/v1/auth/login`

Sample body:
```json
{
  "email": "your_email@example.com",
  "password": "StrongPass123"
}
```

---

### Step 7: Authorize in Swagger
What this means:
- You connect your login token to Swagger so protected APIs can run.

How:
1. Click `Authorize` button in Swagger.
2. Fill login fields (username = your email, password = your password).
3. Click `Authorize` and then `Close`.

---

### Step 8: Add your AI provider API key
What this means:
- You connect your account to an AI provider key (OpenAI, Gemini, Claude, Groq, etc.).
- Backend detects provider automatically.

Where:
- `POST /api/v1/integrations/api-key`

Sample body:
```json
{
  "api_key": "your_real_provider_api_key"
}
```

---

### Step 9: Create chat window
What this means:
- A chat window is a conversation container.
- Every message history is saved inside this conversation.

Where:
- `POST /api/v1/chat/windows`

---

### Step 10: Send prompt to AI
What this means:
- You ask a question and backend routes it to your active provider.

Where:
- `POST /api/v1/chat/route`

Sample body:
```json
{
  "prompt": "Give me a backend roadmap for next 2 weeks"
}
```

---

### Step 11: Check message history
What this means:
- You can verify that chat messages are being stored.

Where:
- `GET /api/v1/chat/conversations/{chat_id}/messages`

Example:
- If response from chat route gave `conversation_id = 14`, call history with chat id `14`.

---

### Step 12: Run smoke test (quick confidence check)
What this means:
- Fast automatic test to confirm major APIs are alive.

Command:
```powershell
.\smoke_check.ps1
```

---

## Swagger UI Explained (Very Simple)

### 1) Top area
- `Authorize` button: connects your login.
- If not authorized, protected APIs give token errors.

### 2) Endpoint blocks (GET, POST, etc.)
- Each block is one backend action.
- `POST` usually sends data.
- `GET` usually reads data.

### 3) Try it out button
- Makes fields editable.
- Without clicking this, you cannot submit custom values.

### 4) Request body box
- This is where you put JSON input.
- Example: email/password/api_key/prompt.

### 5) Execute button
- Sends your request to backend.

### 6) Server response
- Shows status code + response JSON.
- `200/201` = success.
- `400/401/403/404/409/422` = issue, not always code bug.

### 7) Curl section
- Auto-generated command showing exactly what Swagger sent.
- Useful for copying into PowerShell (with small syntax changes if needed).

### 8) Response codes list
- Swagger shows possible outcomes.
- Seeing `422` in docs is normal; it means "possible validation error".

---

## OAuth Login Fields in Swagger (What They Mean)

In `Authorize` popup you may see these fields:

- `grant_type`: authentication method type. For your backend it is password flow. Leave default or `password`.
- `username`: your login email (example: `raushankhemani@gmail.com`).
- `password`: your backend account password.
- `scope`: advanced permission text. Keep empty for now.
- `client_id`: app id for advanced OAuth apps. Keep empty for now.
- `client_secret`: app secret for advanced OAuth apps. Keep empty for now.

For your current backend usage:
- Fill only `username` and `password`.
- Keep the rest empty unless you intentionally add OAuth clients later.

---

## File Guide For Non-Coders (What Each Part Does)

### Root files
- `app.py`: front door of backend app startup.
- `config.py`: all settings from environment (security, DB, limits).
- `requirements.txt`: list of required Python libraries.
- `smoke_check.ps1`: quick automatic health/auth/chat checks.
- `Dockerfile`: lets backend run in a container.
- `alembic.ini`: migration configuration.

### `api/` folder (the visible buttons in Swagger)
- `api/router.py`: combines all route groups into one API tree.
- `api/dependencies.py`: shared checks like login, roles, rate limits.
- `api/routes/auth.py`: account register/login/refresh/me/logout actions.
- `api/routes/integrations.py`: save API key and read active provider.
- `api/routes/chat.py`: create windows, send prompts, read history.
- `api/routes/providers.py`: provider listing and provider operations.
- `api/routes/health.py`: health/readiness for monitoring.

### `services/` folder (actual business brain)
- `auth_service.py`: user auth logic, token creation/validation.
- `integration_service.py`: API key detection and secure storage logic.
- `chat_service.py`: chat flow, latency/tokens/cost logging.
- `provider_gateway.py`: common path to send request to providers.
- `provider_service.py`: provider records and defaults.
- `crypto_service.py`: encrypt/decrypt sensitive key values.

### `providers/` folder (AI connector design)
- `base.py`: standard interface every provider client follows.
- `registry.py`: chooses provider client by provider key.
- `mock_provider.py`: safe simulated provider for local tests.

### `db/` folder (database side)
- `session.py`: DB connection/session lifecycle.
- `init_db.py`: initial table creation and seed setup.
- `models/`: table definitions (`users`, `api_keys`, `chats`, `messages`, `usage_logs`, `refresh_tokens`, `providers`).

### `schemas/` folder (input/output format)
- Defines what each endpoint accepts and returns.
- Prevents broken/missing field data.

### `core/` folder (shared core systems)
- `security.py`: bcrypt hashing + JWT helpers.
- `exceptions.py`: unified error response formatter.
- `logging.py`: structured logs for debugging and analytics.
- `app_factory.py`: app creation and startup wiring.

### `tests/` folder (auto checks)
- Confirms auth/chat/provider endpoints work after changes.

---

## From Where To Get Provider Key (Provider Key Source)

First important point:
- In your backend, `provider_key` is internal name like `chatgpt`, `gemini`, `claude`, `grok`, `groq`.
- You usually do not type this manually if key detection is automatic.
- You provide real `api_key`, backend maps it to provider.

### OpenAI (ChatGPT)
- Go to OpenAI platform API keys page.
- Create a new secret key.
- Key often starts with `sk-` or `sk-proj-`.

### Google Gemini
- Go to Google AI Studio / Google AI API key page.
- Generate API key.
- Usually used for Gemini models.

### Anthropic Claude
- Go to Anthropic Console.
- Create API key from developer/account settings.

### Grok (xAI)
- Go to xAI developer console.
- Create API key there.

### Groq
- Go to Groq Console keys section.
- Create key (often starts with `gsk_`).

### Security rules for keys
- Never share keys in chat/screenshots/commits.
- If leaked once, rotate immediately.
- Store only in backend secure input or environment variables.
