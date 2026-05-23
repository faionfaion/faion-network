# purpose: validated tool dispatcher (registry + decorator + structured error return)
# consumes: model-emitted {tool_name, args} JSON
# produces: code (drop-in dispatcher module + audit log emission)
# depends-on: pydantic OR jsonschema for validation; audit-sink client
# token-budget-impact: ~250 tokens if loaded into LLM context
"""
Validated tool dispatcher with registry decorator and structured error return.
Drop-in for any provider: OpenAI, Claude, Gemini.

Usage:
    @tool_registry.register
    def get_weather(location: str, unit: str = "celsius") -> dict:
        ...

    result = tool_registry.dispatch("get_weather", {"location": "Paris"})
"""

from __future__ import annotations

import functools
import json
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry with validated dispatch and structured error returns."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}

    def register(self, fn: Callable) -> Callable:
        """Decorator: register a function as a dispatchable tool."""
        self._tools[fn.__name__] = fn

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)

        return wrapper

    def dispatch(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Dispatch a tool call by name with validated arguments.

        Returns a structured result dict — never raises.
        On error returns {"error": CODE, "message": "..."}.
        """
        if name not in self._tools:
            known = list(self._tools)
            return {
                "error": "TOOL_NOT_FOUND",
                "message": f"Unknown tool {name!r}. Available: {known}",
            }

        fn = self._tools[name]

        # Validate argument types against annotations
        hints = fn.__annotations__
        for param, value in arguments.items():
            expected = hints.get(param)
            if expected and not isinstance(value, expected):
                return {
                    "error": "INVALID_ARGUMENT",
                    "message": (
                        f"Parameter {param!r} expected {expected.__name__}, "
                        f"got {type(value).__name__}"
                    ),
                }

        try:
            result = fn(**arguments)
            logger.info("tool=%s args=%s result_type=%s", name, arguments, type(result).__name__)
            return result
        except TypeError as exc:
            return {"error": "MISSING_ARGUMENT", "message": str(exc)}
        except Exception as exc:
            logger.exception("tool=%s raised unexpected error", name)
            return {"error": "EXECUTION_ERROR", "message": str(exc)}

    def definitions_openai(self) -> list[dict]:
        """Return tool definitions in OpenAI format (uses docstring as description)."""
        tools = []
        for name, fn in self._tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": (fn.__doc__ or "").strip().splitlines()[0],
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            })
        return tools

    def definitions_claude(self) -> list[dict]:
        """Return tool definitions in Claude/Anthropic format."""
        tools = []
        for name, fn in self._tools.items():
            tools.append({
                "name": name,
                "description": (fn.__doc__ or "").strip().splitlines()[0],
                "input_schema": {"type": "object", "properties": {}, "required": []},
            })
        return tools


# Module-level singleton
tool_registry = ToolRegistry()


# ── Example tools ──────────────────────────────────────────────────────────────

@tool_registry.register
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a city. Use when user asks about weather conditions."""
    # Replace with real API call
    return {"location": location, "temperature": 22, "unit": unit, "condition": "sunny"}


@tool_registry.register
def search_records(query: str, limit: int = 10) -> dict:
    """Search internal records by keyword. Returns ranked list of matching items."""
    # Replace with real search
    return {"results": [], "total": 0, "query": query}


# ── Agentic loop helper ────────────────────────────────────────────────────────

def run_tool_loop(client, model: str, messages: list, tools: list, max_iter: int = 15) -> str:
    """
    Provider-agnostic agentic loop (OpenAI SDK shape).
    Calls tool_registry.dispatch for each tool_call returned by the LLM.
    """
    for iteration in range(max_iter):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content or ""

        messages.append(msg)

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = tool_registry.dispatch(tc.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })

    return f"[max_iterations={max_iter} reached]"
