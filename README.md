# AI Hub Backend

This project is the backend (the "brain and engine room") for an AI Hub app.

If you are new to coding:
- Frontend = what users see and click.
- Backend = what does the real work behind the screen.

In this project, backend handles:
- account creation and login
- security and tokens
- provider selection (ChatGPT, Gemini, Claude, Grok, Groq)
- chat request processing
- chat history saving
- usage/cost logging

---

## 1) What This Backend Is Trying To Solve

Many people want one app where they can switch between multiple AI systems.

This backend is built for exactly that:
- user signs in once
- user can use one provider or switch provider
- chat messages are stored safely
- system can track performance and usage

So this is not "just one chatbot endpoint".  
It is a structured system for a real multi-provider AI product.

---

## 2) What You Get Out Of The Box

- Authentication with JWT access + refresh tokens
- Password hashing with bcrypt
- Role checks (RBAC)
- Per-user rate limiting
- Encrypted API key storage (if BYOK mode is used)
- Real provider integrations (no fake mock replies in runtime path)
- Async provider calls with timeout and retry
- Chat windows + message history
- Usage logs with latency/tokens/cost
- Swagger docs for API testing
- Local Chat UI for simple visual testing
- Alembic migration setup
- Dockerfile for container deployment

---

## 3) How The System Works In Plain Language

Imagine this flow:

1. User logs in.
2. User types a message.
3. Backend checks user token.
4. Backend decides which provider to use.
5. Backend sends request to real provider API.
6. Backend gets response.
7. Backend saves user message + assistant message in DB.
8. Backend saves usage metrics.
9. Backend returns final answer to frontend.

This means your app is not only "talking", it is also recording history and analytics.

---

## 4) Project Structure (Simple Meaning)

### `api/`
HTTP route layer.  
This is where endpoints live (`/auth/login`, `/chat/route`, etc.).

### `services/`
Business logic layer.  
Real decision-making is here (auth rules, chat flow, provider logic).

### `providers/`
Provider connector layer.  
Contains the code that talks to OpenAI, Gemini, Claude, Grok, Groq APIs.

### `db/`
Database layer.  
Contains table models, DB session handling, initial setup.

### `schemas/`
Input/output rules.  
Defines request and response formats so APIs stay clean and predictable.

### `core/`
Shared internals.  
App factory, security helpers, logging, exception handling.

### `tests/`
Automated checks for key routes and backend behavior.

---

## 5) Supported Provider Keys In This Backend

Internal `provider_key` values:
- `chatgpt`
- `gemini`
- `claude`
- `grok`
- `groq`

Note:
- `copilot` may appear in provider metadata, but direct runtime client flow for it is not active in current chat path.

---

## 6) Two Ways To Run Chat In Product

### Mode A: Platform-Managed Keys (Recommended)
You (app owner) keep provider API keys in backend `.env`.

Benefits:
- users do not paste raw provider keys
- cleaner user experience
- easier control and governance

### Mode B: BYOK (Bring Your Own Key)
User adds their own provider key via integration endpoint.

Benefits:
- user pays their own provider usage
- useful for advanced/enterprise users

---

## 7) Requirements Before Running

- Python installed
- Pip working
- Internet access for real provider calls
- At least one real provider API key

---

## 8) First-Time Setup (Step by Step)

Open PowerShell:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
```

Create `.env` file from `.env.example`, then set important values:

- `JWT_SECRET_KEY`
- `API_KEY_ENCRYPTION_KEY`
- `DATABASE_URL` (default sqlite is fine for local)

Add at least one provider key:
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- `XAI_API_KEY`
- `GROQ_API_KEY`

Start backend:

```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

---

## 9) Where To Open It

- Swagger API docs: `http://127.0.0.1:8000/docs`
- Local chat page: `http://127.0.0.1:8000/chat-ui`

---

## 10) Complete Testing Flow (Manual)

### Using Swagger
1. Register user: `POST /api/v1/auth/register`
2. Login user: `POST /api/v1/auth/login`
3. Click `Authorize` and login
4. Chat: `POST /api/v1/chat/route`
5. Copy `chat_id` from response
6. Read history: `GET /api/v1/chat/conversations/{chat_id}/messages`

If you want BYOK mode:
1. Call `POST /api/v1/integrations/api-key`
2. Then use chat endpoints

### Using Chat UI
1. Open `/chat-ui`
2. Register
3. Login
4. Optional: add API key if using BYOK
5. Send prompt
6. Verify reply appears
7. Verify history loads

---

## 11) Automated Testing

Quick smoke test:

```powershell
.\smoke_check.ps1
```

Full tests:

```powershell
python -m pytest -q
```

---

## 12) Database and Migration Notes

Run migrations:

```powershell
alembic upgrade head
```

If local SQLite schema is outdated and gives column errors, recreate local DB:

```powershell
Remove-Item .\ai_hub.db -Force
python -m uvicorn app:app --reload
```

---

## 13) Security Notes (Very Important)

- Never hardcode real API keys in source files.
- Never commit `.env` with secrets.
- If any key is exposed, rotate it immediately.
- Keep JWT secret strong in production.
- Use HTTPS in deployment.
- Prefer managed secret storage in cloud deployments.

---

## 14) Docker (Optional)

Build image:

```powershell
docker build -t ai-hub-backend .
```

Run container:

```powershell
docker run --rm -p 8000:8000 ai-hub-backend
```

---

## 15) What "Production-Ready" Means Here

This backend already includes many production-level foundations:
- layered architecture
- security primitives
- logging and error handling
- retries and timeouts
- data persistence and schema control

Still, final production quality always depends on:
- infra setup
- monitoring stack
- load testing
- cloud secret management
- backup and disaster recovery

---

## 16) For Non-Coders: One-Sentence Summary

This backend is the secure control center of your AI Hub app that manages users, talks to real AI providers, stores conversations, and returns chat responses to your app.

---

## 17) Beginner Version

If you want even simpler explanations, open:
- `README_BEGINNER.md`

