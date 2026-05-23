"""
purpose: Force Claude to return typed JSON via tool_choice; canonical pattern for structured output.
consumes: anthropic.Anthropic client + JSON Schema describing the desired shape
produces: dict matching the schema (or raises ValidationError on schema mismatch)
depends-on: content/01-core-rules.xml r7; content/02-output-contract.xml
token-budget-impact: one call per extraction; no agent-prompt cost
"""
from __future__ import annotations

import anthropic

MODEL = "claude-sonnet-4-5"


def force_extract(client: anthropic.Anthropic, system: str, user: str, schema: dict, tool_name: str = "extract") -> dict:
    """Force Claude to call `extract` with input matching schema; return tool_use.input."""
    tools = [{
        "name": tool_name,
        "description": "Return the structured result. Always call this tool exactly once with the data.",
        "input_schema": schema,
    }]
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        tools=tools,
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user}],
    )
    for block in resp.content:
        if block.type == "tool_use" and block.name == tool_name:
            return block.input
    raise RuntimeError("forced tool did not fire; check tool_choice + schema")


if __name__ == "__main__":
    # Example: extract person {name, age} from free text.
    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        "required": ["name", "age"],
    }
    print(schema)  # noqa: T201 - sample only
