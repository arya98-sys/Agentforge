import pytest
from fastapi.testclient import TestClient

from app.agent.engine import AgentEngine, ToolError
from app.main import app


def test_uppercase_tool_returns_structured_result():
    result = AgentEngine().run("hello", "uppercase")
    assert result["status"] == "succeeded"
    assert result["output"] == "HELLO"
    assert result["trace"][0]["event"] == "tool_started"


def test_reverse_tool():
    assert AgentEngine().run("agent", "reverse")["output"] == "tnega"


def test_unknown_tool_is_rejected():
    with pytest.raises(ToolError, match="unknown tool"):
        AgentEngine().run("hello", "missing")


def test_empty_task_is_rejected():
    with pytest.raises(ToolError, match="non-empty"):
        AgentEngine().run("   ")


def test_tool_exception_is_captured_in_trace():
    def broken(_: str) -> str:
        raise RuntimeError("boom")
    result = AgentEngine(tools={"broken": broken}).run("hello", "broken")
    assert result["status"] == "failed"
    assert result["error"] == "boom"
    assert result["trace"][-1]["event"] == "tool_failed"


def test_health_endpoint():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}


def test_runs_endpoint():
    client = TestClient(app)
    response = client.post("/runs", json={"task": "hi", "tool": "uppercase"})
    assert response.status_code == 200
    assert response.json()["output"] == "HI"
