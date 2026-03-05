import os
import uuid

import pytest
from fastapi.testclient import TestClient

TEST_DB_PATH = "test_ai_hub.db"
os.environ["DATABASE_URL"] = f"sqlite:///./{TEST_DB_PATH}"

from app import app  # noqa: E402
from db.init_db import init_db  # noqa: E402
from providers.base import ProviderResult  # noqa: E402
from services import chat_service  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    init_db()


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def stub_provider_gateway(monkeypatch: pytest.MonkeyPatch):
    async def _fake_generate(provider_key: str, prompt: str, api_key: str | None = None, *, timeout_seconds: int = 20):
        answer = "Hello. How are you?" if prompt.strip().lower() in {"hi", "hello", "hey"} else f"[{provider_key}] {prompt}"
        return ProviderResult(
            text=answer,
            model_name=f"{provider_key}-test-model",
            tokens_in=max(1, len(prompt) // 4),
            tokens_out=max(1, len(answer) // 4),
        )

    monkeypatch.setattr(chat_service.provider_gateway, "generate", _fake_generate)


@pytest.fixture()
def unique_user_payload() -> dict:
    suffix = uuid.uuid4().hex[:8]
    return {
        "email": f"testuser_{suffix}@example.com",
        "password": "StrongPass123",
        "full_name": "Test User",
    }


@pytest.fixture()
def auth_context(client: TestClient, unique_user_payload: dict) -> dict:
    register_res = client.post("/api/v1/auth/register", json=unique_user_payload)
    assert register_res.status_code == 201

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
    )
    assert login_res.status_code == 200
    token_data = login_res.json()["data"]
    return {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "headers": {"Authorization": f"Bearer {token_data['access_token']}"},
    }
