from fastapi.testclient import TestClient


def test_register_login_me_flow(client: TestClient, unique_user_payload: dict) -> None:
    register_res = client.post("/api/v1/auth/register", json=unique_user_payload)
    assert register_res.status_code == 201

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == unique_user_payload["email"]


def test_token_form_login(client: TestClient, unique_user_payload: dict) -> None:
    register_res = client.post("/api/v1/auth/register", json=unique_user_payload)
    assert register_res.status_code == 201

    token_res = client.post(
        "/api/v1/auth/token",
        data={"username": unique_user_payload["email"], "password": unique_user_payload["password"]},
    )
    assert token_res.status_code == 200
    assert "access_token" in token_res.json()
