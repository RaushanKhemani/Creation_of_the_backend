from fastapi.testclient import TestClient


def test_providers_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/providers")
    assert response.status_code == 401


def test_providers_list_with_auth(client: TestClient, auth_context: dict) -> None:
    response = client.get("/api/v1/providers", headers=auth_context["headers"])
    assert response.status_code == 200
    items = response.json()["data"]
    assert isinstance(items, list)
    assert len(items) >= 1
