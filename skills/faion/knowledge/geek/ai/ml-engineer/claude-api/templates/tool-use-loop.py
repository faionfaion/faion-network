# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

# Complete tool-use skeleton: ToolExecutor + retry + forced structured output
import json
import random
import time
from typing import Any, Callable

import anthropic

client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

class ToolExecutor:
    """Register tools and dispatch Claude's tool_use blocks."""

    def __init__(self):
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable[..., Any]] = {}

    def register(self, tool: dict, handler: Callable[..., Any]) -> None:
        self._tools[tool["name"]] = tool
        self._handlers[tool["name"]] = handler

    @property
    def tools(self) -> list[dict]:
        return list(self._tools.values())

    def execute(self, name: str, inputs: dict) -> tuple[str, bool]:
        """Execute a tool. Returns (content_str, is_error)."""
        if name not in self._handlers:
            return json.dumps({"error": f"Unknown tool: {name}"}), True
        try:
            result = self._handlers[name](**inputs)
            return json.dumps({"result": result}), False
        except Exception as exc:
            return json.dumps({"error": str(exc)}), True


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------

def _with_backoff(fn: Callable, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return fn()
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
        except anthropic.APIError as e:
            if e.status_code < 500 or attempt == max_retries - 1:
                raise
        wait = min(2 ** attempt + random.uniform(0, 1), 60)
        time.sleep(wait)
    raise RuntimeError("Max retries exceeded")


# ---------------------------------------------------------------------------
# Standard tool-use loop
# ---------------------------------------------------------------------------

def run_with_tools(
    prompt: str,
    executor: ToolExecutor,
    model: str = "claude-sonnet-4-20250514",
    system: str | None = None,
    max_tokens: int = 4096,
    max_turns: int = 10,
) -> str:
    """Run a tool-use conversation. Returns final text response."""
    messages: list[dict] = [{"role": "user", "content": prompt}]

    for turn in range(max_turns):
        create_kwargs: dict[str, Any] = dict(
            model=model,
            max_tokens=max_tokens,
            tools=executor.tools,
            messages=messages,
        )
        if system:
            create_kwargs["system"] = system

        response = _with_backoff(lambda: client.messages.create(**create_kwargs))

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason != "tool_use":
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                content, is_error = executor.execute(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content,
                    "is_error": is_error,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"Tool loop exceeded {max_turns} turns without reaching end_turn")


# ---------------------------------------------------------------------------
# Forced structured output (use a tool schema to guarantee JSON shape)
# ---------------------------------------------------------------------------

OUTPUT_SCHEMA: dict = {
    "name": "structured_output",
    "description": "Return the final structured result. Always call this tool to respond.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "sources": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["summary", "confidence", "sources"],
    },
}


def extract_structured(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
) -> dict:
    """Force Claude to return a structured dict matching OUTPUT_SCHEMA."""
    response = _with_backoff(lambda: client.messages.create(
        model=model,
        max_tokens=max_tokens,
        tools=[OUTPUT_SCHEMA],
        tool_choice={"type": "tool", "name": OUTPUT_SCHEMA["name"]},
        messages=[{"role": "user", "content": prompt}],
    ))
    for block in response.content:
        if block.type == "tool_use" and block.name == OUTPUT_SCHEMA["name"]:
            return block.input
    raise RuntimeError("Structured output tool was not called")


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    executor = ToolExecutor()

    # Register a sample tool
    executor.register(
        {
            "name": "lookup_policy",
            "description": "Look up a company policy by topic.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Policy topic, e.g. 'refunds'"}
                },
                "required": ["topic"],
            },
        },
        handler=lambda topic: f"Policy for '{topic}': 30-day full refund for unopened items.",
    )

    # Standard tool-use loop
    answer = run_with_tools(
        prompt="What is the refund policy for unopened items?",
        executor=executor,
        system="You are a helpful customer service agent.",
    )
    print("Answer:", answer)

    # Forced structured output
    result = extract_structured(
        "Summarize: Claude is an AI assistant by Anthropic focused on safety and helpfulness."
    )
    print("Structured:", result)
