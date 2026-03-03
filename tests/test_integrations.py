from fastapi.testclient import TestClient


def test_api_key_registration_and_active_provider(client: TestClient, auth_token: str) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}

    register_res = client.post(
        "/api/v1/integrations/api-key",
        json={"api_key": "sk-test-openai-key-123456"},
        headers=headers,
    )
    assert register_res.status_code == 200
    payload = register_res.json()
    assert payload["provider_key"] == "chatgpt"
    assert payload["chat_enabled"] is True

    active_res = client.get("/api/v1/integrations/active", headers=headers)
    assert active_res.status_code == 200
    active_payload = active_res.json()
    assert active_payload["provider_key"] == "chatgpt"
    assert active_payload["is_active"] is True
