# Claude Tool Use

## Summary

**One-sentence:** Produces a working Claude tool-use loop — typed JSON Schema tool definitions, canonical agent loop with parallel tool dispatch, forced-tool structured output, max-iteration guard.

**One-paragraph:** Claude tool use (function calling) is the canonical mechanism for letting Claude call external APIs, databases, and search. The reliable shape: define tools with explicit JSON Schema `input_schema`; detect `stop_reason == "tool_use"` and continue the loop; append the full `response.content` list (text + tool_use blocks) as the assistant turn so conversation history stays parseable; cap iterations at 10-20 to avoid runaways; execute parallel tool_use blocks concurrently and return all results in one user message; use `tool_choice={"type":"tool","name":"X"}` to force typed structured output via the tool-use pathway. MCP exists for Claude Desktop (stdio) — programmatic API users should stay on standard tool use.

**Ефективно для:** agents fetching live data, structured-output extraction, parallel API dispatch, code-execution wrappers, function-call routing.

## Applies If (ALL must hold)

- Claude API is the model under integration (Anthropic SDK).
- Agent needs to call ≥1 external function and incorporate the result.
- Caller can store conversation history and re-send it on each turn.
- A max-iteration cap is acceptable (no genuinely unbounded loops needed).

## Skip If (ANY kills it)

- Pure text completion with no external data.
- Using OpenAI / Gemini SDK — refer to `[[function-calling-patterns]]` or `[[gemini-function-calling]]`.
- Streaming-only UX where the loop cannot wait for `stop_reason`.
- &gt;20 tools — Claude routinely picks wrong; route via a meta-tool selector first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool list with schemas | JSON | tools registry / `tools.json` |
| Anthropic API key | secret | env var `ANTHROPIC_API_KEY` |
| Tool executor function | callable | application code |
| System prompt | string | prompt repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[function-calling-patterns]]` | Cross-vendor patterns context. |
| `[[guardrails-implementation]]` | Output guardrails apply to tool-call results. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: schema flatness, stop_reason check, max-turns, append full content, parallel exec, errors-as-content, force-tool for typed output, MCP scope | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for a tool definition + agent-loop trace format | ~700 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: deep nesting, append-text-only, blind indexing, infinite loop, strict additionalProperties, MCP-in-server, thinking-blocks-in-tool_result | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: design tool schemas → write executor → write agent loop → set max-turns → handle errors → add forced-tool extraction | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "is the model Claude AND ≥1 tool call required?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Write tool schema from spec | sonnet | Mechanical mapping. |
| Implement executor | sonnet | Bounded code generation. |
| Run loop and tool calls | runtime | (not an LLM task) |
| Triage tool-call error | opus | Multi-block reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/tool-definition.json` | One tool definition with JSON Schema input_schema. |
| `templates/agent-loop.py` | Reference Python agent loop with parallel tool dispatch + max-turns guard. |
| `templates/forced-tool-extract.py` | tool_choice extraction pattern for typed JSON output. |
| `templates/_smoke-test.json` | Minimum-valid tool definition for the validator. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-claude-tool-use.py` | Validates tool-definition JSON Schema (flat, additionalProperties allowed, required arrays correct). | Pre-commit on tool definitions. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[function-calling-patterns]]`
- `[[gemini-function-calling]]`
- `[[guardrails-implementation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether to use this Claude-specific pattern: non-Claude models route to `[[function-calling-patterns]]` or vendor-specific siblings; streaming-only UX → use streaming response API directly; ≤1 tool call → bypass the loop and call directly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool-definition.json`

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location. Call this when the user asks about weather or temperature in a specific city.",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name with country code, e.g., 'Kyiv, UA' or 'London, UK'"
      },
      "unit": {
        "type": "string",
        "enum": [
          "celsius",
          "fahrenheit"
        ],
        "description": "Temperature unit for the response"
      }
    },
    "required": [
      "location"
    ]
  }
}
```

### `templates/agent-loop.py`

```python
Canonical Claude agentic loop with parallel tool execution.

Usage:
    tools = [{"name": "...", "description": "...", "input_schema": {...}}]
    result = run_agent_loop(client, tools, execute_fn, user_input)
"""
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
import anthropic

MODEL = "claude-sonnet-4-20250514"
MAX_TURNS = 15


def run_agent_loop(
    client: anthropic.Anthropic,
    tools: list[dict],
    execute_fn: Callable[[str, dict], str],
    user_input: str,
    system: str = "",
) -> str:
    """Run the agentic loop. Returns the final text response."""
    messages = [{"role": "user", "content": user_input}]

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages,
        )
        # Append full content list (includes tool_use blocks)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break

        # Execute all tool calls in parallel
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        with ThreadPoolExecutor() as executor:
            futures = {b.id: executor.submit(execute_fn, b.name, b.input) for b in tool_uses}

        results = [
            {"type": "tool_result", "tool_use_id": bid, "content": f.result()}
            for bid, f in futures.items()
        ]
        messages.append({"role": "user", "content": results})

    return next(
        (b.text for b in response.content if b.type == "text"),
        "",
    )


def safe_execute(name: str, input_data: dict) -> str:
    """Example tool executor — replace with real implementations."""
    try:
        if name == "example_tool":
            return json.dumps({"result": "ok"})
        return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e), "tool": name})
```

### `templates/forced-tool-extract.py`

```python
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
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid Claude tool definition for the validator.",
  "_consumes": "validate-claude-tool-use.py",
  "_produces": "ok verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "docs-only",
  "name": "get_weather",
  "description": "Get current weather for a location. Call this when the user asks about weather or temperature.",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name with country code"
      },
      "unit": {
        "type": "string",
        "enum": [
          "celsius",
          "fahrenheit"
        ]
      }
    },
    "required": [
      "location"
    ]
  }
}
```
