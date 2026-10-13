# AgentForge

An evaluation-first platform for building, running, and benchmarking AI agents.

AgentForge focuses on reliable agent engineering: bounded execution, explicit tool interfaces, traceable runs, automated tests, and measurable evaluation rather than a chat-only demo.

## Planned architecture

- FastAPI backend for submitting tasks and inspecting runs
- Agent execution engine with bounded steps, a tool registry, structured traces, and error handling
- PostgreSQL persistence for run history
- Evaluation suite for task success, latency, token usage, and provider-reported cost where available
- React dashboard for run inspection and benchmark comparison
- Docker and deployment after the core behavior is tested

## Roadmap

1. Establish a tested backend foundation.
2. Implement a bounded multi-step agent loop and extensible tool registry.
3. Persist runs and expose clear API schemas.
4. Add repeatable benchmark tasks and evaluation metrics.
5. Build a dashboard for inspecting traces and comparing runs.
6. Document deployment and operational trade-offs.

## Development

Use Python 3.12 or newer in a virtual environment.

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

The API health endpoint is `GET /health`; `GET /runs` returns the current in-memory run list. The initial engine milestone is deterministic and does not call an LLM. Keep secrets out of source control and use environment variables for future provider credentials.

## Quality bar

Every milestone should include tests, explicit failure behavior, clear documentation, and honest reporting of what is implemented versus planned. Benchmark results should be reproducible and should not imply capabilities that have not been measured.
