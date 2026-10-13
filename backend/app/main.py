"""HTTP API for the AgentForge starter backend."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agent.engine import AgentEngine, ToolError

app = FastAPI(title="AgentForge API", version="0.1.0")
engine = AgentEngine()
runs: list[dict] = []


class RunRequest(BaseModel):
    task: str = Field(min_length=1, description="Task text to process")
    tool: str = Field(default="uppercase", description="Registered tool name")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/runs")
def create_run(request: RunRequest) -> dict:
    try:
        result = engine.run(request.task, request.tool)
    except ToolError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    runs.append(result)
    return result


@app.get("/runs")
def list_runs() -> dict[str, list[dict]]:
    return {"runs": runs}
