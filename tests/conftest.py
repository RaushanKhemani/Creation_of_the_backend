import uuid

import pytest
from fastapi.testclient import TestClient

from app import app
from db.init_db import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    init_db()


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def unique_user_payload() -> dict:
    suffix = uuid.uuid4().hex[:8]
    return {
        "email": f"testuser_{suffix}@example.com",
        "password": "StrongPass123",
        "full_name": "Test User",
    }


@pytest.fixture()
def auth_token(client: TestClient, unique_user_payload: dict) -> str:
    register_res = client.post("/api/v1/auth/register", json=unique_user_payload)
    assert register_res.status_code == 201

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
    )
    assert login_res.status_code == 200
    return login_res.json()["access_token"]
