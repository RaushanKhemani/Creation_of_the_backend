from fastapi.testclient import TestClient


def test_providers_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/providers")
    assert response.status_code == 400


def test_providers_list_with_auth(client: TestClient, auth_token: str) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/v1/providers", headers=headers)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1
