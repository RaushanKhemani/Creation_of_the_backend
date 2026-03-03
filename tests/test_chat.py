from fastapi.testclient import TestClient


def test_chat_route_and_history(client: TestClient, auth_token: str) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    api_key_res = client.post("/api/v1/integrations/api-key", json={"api_key": "sk-test-integration-key-12345"}, headers=headers)
    assert api_key_res.status_code == 200

    route_res = client.post(
        "/api/v1/chat/route",
        json={"prompt": "Design backend milestones for 30 days."},
        headers=headers,
    )
    assert route_res.status_code == 200
    route_payload = route_res.json()
    assert "conversation_id" in route_payload
    assert "answer" in route_payload

    conversation_id = route_payload["conversation_id"]
    history_res = client.get(f"/api/v1/chat/conversations/{conversation_id}/messages", headers=headers)
    assert history_res.status_code == 200
    messages = history_res.json()
    assert len(messages) >= 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
