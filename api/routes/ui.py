from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

CHAT_UI_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Hub Local Chat</title>
  <style>
    :root {
      --bg: #f6f8fb;
      --card: #ffffff;
      --text: #111827;
      --muted: #6b7280;
      --accent: #0f766e;
      --border: #d1d5db;
      --danger: #b91c1c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      background: linear-gradient(160deg, #f4f8ff 0%, #ecfeff 100%);
      color: var(--text);
    }
    .container {
      max-width: 980px;
      margin: 24px auto;
      padding: 0 14px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 12px;
    }
    h1 { margin: 0 0 10px; font-size: 24px; }
    h2 { margin: 0 0 8px; font-size: 16px; }
    p { margin: 8px 0; color: var(--muted); }
    .row {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 8px;
    }
    .c4 { grid-column: span 4; }
    .c6 { grid-column: span 6; }
    .c8 { grid-column: span 8; }
    .c12 { grid-column: span 12; }
    input, select, button, textarea {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px;
      font-size: 14px;
      font-family: inherit;
      background: #fff;
    }
    textarea { min-height: 88px; resize: vertical; }
    button {
      background: var(--accent);
      color: #fff;
      border: none;
      cursor: pointer;
      font-weight: 600;
    }
    button.secondary {
      background: #334155;
    }
    .messages {
      border: 1px solid var(--border);
      border-radius: 10px;
      min-height: 240px;
      max-height: 420px;
      overflow: auto;
      padding: 10px;
      background: #f9fafb;
    }
    .msg {
      margin: 8px 0;
      padding: 8px 10px;
      border-radius: 8px;
      background: #fff;
      border: 1px solid #e5e7eb;
    }
    .role {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }
    .ok { color: #065f46; }
    .err { color: var(--danger); white-space: pre-wrap; }
    .mono { font-family: Consolas, monospace; font-size: 12px; word-break: break-all; }
    @media (max-width: 760px) {
      .c4, .c6, .c8, .c12 { grid-column: span 12; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Hub Local Chat UI</h1>
    <p>Use this page to test your backend end-to-end without Swagger.</p>

    <div class="card">
      <h2>1) Account</h2>
      <div class="row">
        <div class="c4"><input id="email" placeholder="Email" /></div>
        <div class="c4"><input id="password" type="password" placeholder="Password" /></div>
        <div class="c4"><input id="fullName" placeholder="Full name (for register)" /></div>
        <div class="c6"><button onclick="registerUser()">Register</button></div>
        <div class="c6"><button class="secondary" onclick="loginUser()">Login</button></div>
      </div>
      <p id="authStatus"></p>
      <p class="mono" id="tokenView"></p>
    </div>

    <div class="card">
      <h2>2) Connect Provider API Key (Optional)</h2>
      <div class="row">
        <div class="c8"><input id="apiKey" type="password" placeholder="Paste provider API key (OpenAI/Gemini/Claude/Grok/Groq)" /></div>
        <div class="c4"><button onclick="saveApiKey()">Save API Key</button></div>
      </div>
      <div class="row">
        <div class="c6"><button class="secondary" onclick="loadActiveProvider()">Get Active Provider</button></div>
        <div class="c6"><input id="activeProvider" readonly placeholder="Active provider appears here" /></div>
      </div>
      <p id="providerStatus">If your backend has platform keys in `.env`, you can skip this step.</p>
    </div>

    <div class="card">
      <h2>3) Chat</h2>
      <div class="row">
        <div class="c4">
          <select id="providerKey">
            <option value="">Auto (active provider)</option>
            <option value="chatgpt">chatgpt</option>
            <option value="gemini">gemini</option>
            <option value="claude">claude</option>
            <option value="grok">grok</option>
            <option value="groq">groq</option>
            <option value="copilot">copilot</option>
          </select>
        </div>
        <div class="c4"><input id="chatId" placeholder="chat_id (optional)" /></div>
        <div class="c4"><button class="secondary" onclick="loadHistory()">Load History</button></div>
        <div class="c12"><textarea id="prompt" placeholder="Type message. Example: hello"></textarea></div>
        <div class="c12"><button onclick="sendPrompt()">Send</button></div>
      </div>
      <p id="chatStatus"></p>
      <div class="messages" id="messages"></div>
    </div>
  </div>

  <script>
    const BASE = window.location.origin + "/api/v1";
    let token = localStorage.getItem("aihub_access_token") || "";

    function show(id, text, ok = true) {
      const el = document.getElementById(id);
      el.textContent = text;
      el.className = ok ? "ok" : "err";
    }

    function refreshTokenView() {
      const t = token ? token.slice(0, 24) + "... (stored in this browser)" : "No token yet";
      document.getElementById("tokenView").textContent = t;
    }

    async function api(path, method = "GET", body = null, needsAuth = true) {
      const headers = { "Content-Type": "application/json" };
      if (needsAuth) {
        if (!token) throw new Error("Please login first.");
        headers["Authorization"] = "Bearer " + token;
      }
      const res = await fetch(BASE + path, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
      });
      let payload = null;
      const text = await res.text();
      try { payload = text ? JSON.parse(text) : {}; } catch (_) { payload = { raw: text }; }
      if (!res.ok) {
        const msg = payload?.detail || payload?.error?.message || JSON.stringify(payload);
        throw new Error(msg);
      }
      return payload;
    }

    async function registerUser() {
      try {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const full_name = document.getElementById("fullName").value.trim() || "AI Hub User";
        await api("/auth/register", "POST", { email, password, full_name }, false);
        show("authStatus", "Register successful. Now click Login.");
      } catch (e) {
        show("authStatus", "Register failed: " + e.message, false);
      }
    }

    async function loginUser() {
      try {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const res = await api("/auth/login", "POST", { email, password }, false);
        token = res.data.access_token;
        localStorage.setItem("aihub_access_token", token);
        refreshTokenView();
        show("authStatus", "Login successful.");
      } catch (e) {
        show("authStatus", "Login failed: " + e.message, false);
      }
    }

    async function saveApiKey() {
      try {
        const apiKey = document.getElementById("apiKey").value.trim();
        const res = await api("/integrations/api-key", "POST", { api_key: apiKey }, true);
        document.getElementById("activeProvider").value = res.data.provider_key;
        show("providerStatus", "API key saved. Provider detected: " + res.data.provider_key);
      } catch (e) {
        show("providerStatus", "API key save failed: " + e.message, false);
      }
    }

    async function loadActiveProvider() {
      try {
        const res = await api("/integrations/active", "GET", null, true);
        document.getElementById("activeProvider").value = res.data.provider_key;
        show("providerStatus", "Active provider: " + res.data.provider_key);
      } catch (e) {
        show("providerStatus", "Load active provider failed: " + e.message, false);
      }
    }

    function addMessage(role, content) {
      const wrap = document.getElementById("messages");
      const item = document.createElement("div");
      item.className = "msg";
      item.innerHTML = '<div class="role">' + role + '</div><div>' + content.replace(/</g, "&lt;") + "</div>";
      wrap.appendChild(item);
      wrap.scrollTop = wrap.scrollHeight;
    }

    async function sendPrompt() {
      try {
        const prompt = document.getElementById("prompt").value.trim();
        if (!prompt) throw new Error("Prompt is empty.");
        const provider = document.getElementById("providerKey").value.trim();
        const chatIdRaw = document.getElementById("chatId").value.trim();
        const body = { prompt };
        if (provider) body.provider_key = provider;
        if (chatIdRaw) body.chat_id = Number(chatIdRaw);

        addMessage("user", prompt);
        document.getElementById("prompt").value = "";

        const res = await api("/chat/route", "POST", body, true);
        document.getElementById("chatId").value = String(res.data.chat_id);
        addMessage("assistant (" + res.data.provider_key + ")", res.data.answer);
        show("chatStatus", "Reply received. chat_id: " + res.data.chat_id);
      } catch (e) {
        show("chatStatus", "Chat failed: " + e.message, false);
      }
    }

    async function loadHistory() {
      try {
        const chatIdRaw = document.getElementById("chatId").value.trim();
        if (!chatIdRaw) throw new Error("Enter a chat_id first.");
        const res = await api("/chat/conversations/" + chatIdRaw + "/messages", "GET", null, true);
        const wrap = document.getElementById("messages");
        wrap.innerHTML = "";
        for (const m of res.data) addMessage(m.role, m.content);
        show("chatStatus", "History loaded. Messages: " + res.data.length);
      } catch (e) {
        show("chatStatus", "History failed: " + e.message, false);
      }
    }

    refreshTokenView();
  </script>
</body>
</html>
"""


@router.get("/chat-ui", include_in_schema=False)
def chat_ui() -> HTMLResponse:
    return HTMLResponse(CHAT_UI_HTML)
