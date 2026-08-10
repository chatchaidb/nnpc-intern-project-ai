"""API tests that run without a live vLLM server."""

from fastapi.testclient import TestClient

from app.agents import AGENTS
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_agents_returns_all_four():
    response = client.get("/api/agents")
    assert response.status_code == 200
    keys = {agent["key"] for agent in response.json()}
    assert keys == set(AGENTS) == {"customer-service", "marketing", "sales", "finance"}


def test_chat_with_unknown_agent_is_404():
    response = client.post(
        "/api/chat",
        json={"agent": "nope", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert response.status_code == 404
