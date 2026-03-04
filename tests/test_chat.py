from fastapi.testclient import TestClient


def test_chat_route_and_history(client: TestClient, auth_context: dict) -> None:
    headers = auth_context["headers"]
    api_key_res = client.post(
        "/api/v1/integrations/api-key",
        json={"api_key": "sk-test-integration-key-12345"},
        headers=headers,
    )
    assert api_key_res.status_code == 200

    route_res = client.post(
        "/api/v1/chat/route",
        json={"prompt": "Design backend milestones for 30 days."},
        headers=headers,
    )
    assert route_res.status_code == 200
    route_payload = route_res.json()["data"]
    assert "chat_id" in route_payload
    assert "answer" in route_payload

    chat_id = route_payload["chat_id"]
    history_res = client.get(f"/api/v1/chat/conversations/{chat_id}/messages", headers=headers)
    assert history_res.status_code == 200
    messages = history_res.json()["data"]
    assert len(messages) >= 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
