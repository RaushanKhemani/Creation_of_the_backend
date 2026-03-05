# AI Hub Backend - Beginner Friendly Guide

This file is written for people who are completely new to coding.

If you have never used backend, API, Swagger, token, or database before, this guide is for you.

---

## 1) What Is Backend In Very Simple Words

Think of an app like a restaurant:
- Frontend = waiter and menu you can see.
- Backend = kitchen where actual food is prepared.

In your project:
- Frontend is what users will click and view.
- Backend is what handles login, chat requests, provider calls, and message saving.

So backend is invisible to users, but it is the most important working part.

---

## 2) What This Backend Does For Your AI Hub

This backend can:
- create accounts
- log in users
- verify user identity using secure tokens
- connect to AI providers
- route chat message to selected provider
- return answer back
- save full chat history
- save usage stats (time/tokens/cost)

This is why your app can become a real multi-provider AI product.

---

## 3) Important Words You Will See

- `API`: a communication method between systems.
- `Endpoint`: one specific API path like `/api/v1/auth/login`.
- `Token`: temporary secure pass after login.
- `Database`: storage for users/messages/history.
- `Provider`: AI engine like ChatGPT/Gemini/Claude.
- `Rate limit`: request limit to protect server.
- `Swagger`: webpage to test backend APIs by clicking buttons.

---

## 4) Where You Can Open And Use Backend

After server starts:
- Swagger docs: `http://127.0.0.1:8000/docs`
- Chat UI page: `http://127.0.0.1:8000/chat-ui`

Use Swagger when you want detailed API testing.
Use Chat UI when you want a simple conversation screen.

---

## 5) Start Backend (First Time Setup)

Open PowerShell and run:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

If you see:
- `Uvicorn running on http://127.0.0.1:8000`

then backend is ON.

Do not close this PowerShell window while testing.

---

## 6) Environment File (`.env`) In Simple Terms

`.env` is a private settings file for secrets and configuration.

You should keep:
- JWT secret
- encryption key
- database URL
- provider API keys

Never upload real `.env` to public GitHub.

---

## 7) Two Ways To Use Provider Keys

### A) Platform Mode (recommended)
You keep keys in backend `.env`.
Users do not enter provider keys manually.

### B) BYOK mode (optional)
User enters own provider key through API.

For normal consumer app experience, Platform Mode is better.

---

## 8) How To Test In Swagger (Step by Step)

### Step 1: Register account
Endpoint:
- `POST /api/v1/auth/register`

Body example:
```json
{
  "email": "you@example.com",
  "password": "StrongPass123",
  "full_name": "Your Name"
}
```

### Step 2: Login
Endpoint:
- `POST /api/v1/auth/login`

Body example:
```json
{
  "email": "you@example.com",
  "password": "StrongPass123"
}
```

### Step 3: Authorize
In Swagger top-right, click `Authorize`.

Fill:
- `username` = your email
- `password` = your password

Leave these empty for now:
- `scope`
- `client_id`
- `client_secret`

Then click `Authorize`.

### Step 4: Send chat prompt
Endpoint:
- `POST /api/v1/chat/route`

Body example:
```json
{
  "prompt": "Give me a 2-week backend roadmap"
}
```

### Step 5: Read history
Take returned `chat_id`, then call:
- `GET /api/v1/chat/conversations/{chat_id}/messages`

If this works, your chat flow is working end-to-end.

---

## 9) How To Test In Chat UI (Easy Way)

1. Open `http://127.0.0.1:8000/chat-ui`
2. Register
3. Login
4. Send prompt like `hello` or a full question
5. Check reply appears
6. Check history loads

This is the easiest way for non-coders to validate real chat behavior.

---

## 10) Why You Sometimes See 422 In Swagger

`422 Validation Error` usually means:
- required field missing
- wrong field type
- wrong JSON format

It does not always mean backend code is broken.
It often means request format is incorrect.

---

## 11) Why You Sometimes See 401

`401 Unauthorized` usually means:
- token missing
- token expired
- token typed incorrectly
- not authorized in Swagger

Fix:
1. Login again
2. Click `Authorize`
3. Retry endpoint

---

## 12) Provider Key vs API Key (Common Confusion)

`api_key`:
- real secret key from provider account
- example from OpenAI, Google, Anthropic, xAI, Groq

`provider_key`:
- internal backend label
- examples: `chatgpt`, `gemini`, `claude`, `grok`, `groq`

You normally provide `api_key`.
Backend identifies and uses `provider_key`.

---

## 13) Where To Get Real Provider API Keys

- OpenAI (ChatGPT): OpenAI platform API keys page
- Gemini: Google AI Studio / Google AI API keys page
- Claude: Anthropic Console
- Grok: xAI developer console
- Groq: Groq console key page

Always keep keys private.

---

## 14) File Guide In Very Simple Language

### Root files
- `app.py`: starts backend app.
- `config.py`: keeps all settings.
- `requirements.txt`: package list.
- `smoke_check.ps1`: quick health test script.
- `README.md`: main project guide.
- `README_BEGINNER.md`: this beginner guide.

### `api/`
All API endpoints that frontend or Swagger calls.

### `services/`
Core logic of auth/chat/provider behavior.

### `providers/`
Code that talks to real AI provider APIs.

### `db/`
Database setup and table models.

### `schemas/`
Rules for input/output JSON structure.

### `core/`
Security, errors, logging, app startup.

### `tests/`
Automated checks for backend behavior.

---

## 15) What Is Saved In Database

- user account details
- encrypted user provider keys (if BYOK)
- chat windows
- message history
- usage logs (latency/tokens/cost)
- refresh token records
- provider records

This means user conversations are not lost between requests.

---

## 16) Quick Health Check Commands

In new PowerShell:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
.\smoke_check.ps1
python -m pytest -q
```

If both pass and chat works in `/chat-ui`, backend is in good shape.

---

## 17) If You See Database Column Errors

Sometimes old local DB file does not match new code.

Fix by recreating local DB:

```powershell
cd "C:\Users\ASUS\Desktop\ai-hub-backend"
Remove-Item .\ai_hub.db -Force
python -m uvicorn app:app --reload
```

---

## 18) Security Rules You Must Follow

- Never share real API keys in screenshot/chat/GitHub.
- Never commit `.env` containing secrets.
- If secret leaks, rotate immediately.
- Use strong passwords and strong JWT secret.
- Use HTTPS in production.

---

## 19) What Is Still Needed For Final Public Launch

Backend code is strong, but final launch also needs:
- stable cloud deployment
- monitoring dashboards
- alerting
- backup policy
- frontend polish
- billing and quota strategy

This is normal for every serious app.

---

## 20) One-Line Summary

This backend is the secure working brain of your AI Hub that logs users in, talks to real AI providers, stores chats, and returns responses to your app.

