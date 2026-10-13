"""A small deterministic agent runner used as the first tested milestone.

This intentionally does not call an LLM yet. The explicit tool map makes execution
predictable while the project builds toward bounded multi-step agent runs.
"""
from dataclasses import dataclass, field
from typing import Any, Callable


class ToolError(ValueError):
    """Raised when a requested tool or its input is invalid."""


@dataclass
class AgentEngine:
    tools: dict[str, Callable[[str], str]] = field(default_factory=lambda: {
        "uppercase": str.upper,
        "reverse": lambda value: value[::-1],
    })

    def run(self, task: str, tool: str = "uppercase") -> dict[str, Any]:
        """Run one registered tool and return a structured result and trace."""
        if not isinstance(task, str) or not task.strip():
            raise ToolError("task must be a non-empty string")
        if tool not in self.tools:
            raise ToolError(f"unknown tool: {tool}")
        event = {"event": "tool_started", "tool": tool}
        try:
            output = self.tools[tool](task)
        except Exception as exc:
            return {
                "task": task,
                "tool": tool,
                "status": "failed",
                "output": None,
                "error": str(exc),
                "trace": [event, {"event": "tool_failed", "error": str(exc)}],
            }
        return {
            "task": task,
            "tool": tool,
            "status": "succeeded",
            "output": output,
            "error": None,
            "trace": [event, {"event": "tool_completed"}],
        }
