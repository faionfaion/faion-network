# Function Calling Patterns

## Summary

**One-sentence:** Produces a cross-vendor function-calling design — parallel tool dispatch, tool router, agentic loop with bounded iterations, argument validation, schema-enforced output extraction.

**One-paragraph:** Function calling is the canonical mechanism for letting an LLM take actions in external systems. Production patterns generalise across Anthropic (`tool_use`/`tool_result` blocks) and OpenAI (`tool_calls` in assistant message): keep individual tool count ≤20 per request and use a tool router when more exist; validate arguments against the JSON Schema BEFORE execution; cap the agent loop at 10-20 iterations; execute parallel tool_use blocks concurrently; return errors as content for recoverable failures so the model can self-correct. Prefer this pattern over prompt-based JSON parsing for any task where schema correctness matters.

**Ефективно для:** agents calling APIs/DB/filesystem, structured-output extraction, parallel I/O dispatch, multi-step agentic plans, vendor-portable AI features.

## Applies If (ALL must hold)

- Agent must take ≥1 action in an external system OR produce schema-validated structured output.
- Tool count is finite and enumerable (not dynamic per-request).
- Caller can store conversation state across turns.
- Either Anthropic or OpenAI SDK is the integration target.

## Skip If (ANY kills it)

- Pure Q&A with no external action and no schema needs.
- Streaming-first UX where every token must surface immediately.
- Tool set is dynamic and changes per request — invest in a registry first.
- Specifically Claude — use `[[claude-tool-use]]` for the Claude-specific shape.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool registry | JSON Schema per tool | application code |
| Vendor SDK keys | secrets | env / secrets manager |
| Argument validator | jsonschema or pydantic | dependencies |
| Conversation store | dict / DB | session layer |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[claude-tool-use]]` | Claude-specific subset. |
| `[[guardrails-implementation]]` | Output guardrails layer on top of tool returns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 rules: ≤20 tools, validate args before exec, bounded loop, parallel dispatch, errors-as-content, single-vendor format per call, schema-versioned tools | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for tool registry entry + agent-loop trace | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: 50-tool dump, no arg validation, sequential dispatch, infinite loop, vendor mixing, schema-versionless | ~700 |
| `content/04-procedure.xml` | medium | 6-step: design tools → wire validator → write router → write loop → handle errors → eval | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "vendor in {Anthropic, OpenAI} AND ≥1 tool call?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Author tool schemas | sonnet | Mechanical from API specs. |
| Implement router | sonnet | Pattern code. |
| Write agent loop | sonnet | Recipe code. |
| Debug tool-call error | opus | Multi-step reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/tool-registry.schema.json` | JSON Schema for one registry entry. |
| `templates/agent-loop.py` | Cross-vendor reference loop (dispatch via adapter). |
| `templates/argument-validator.py` | Pre-execution arg validator using jsonschema. |
| `templates/tool-router.py` | Two-stage router: category selection → tool dispatch. |
| `templates/_smoke-test.json` | Minimum valid tool registry entry. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-function-calling-patterns.py` | Validates tool-registry entries against schema; asserts each tool has version + schema. | Pre-commit on registry files. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-tool-use]]`
- `[[gemini-function-calling]]`
- `[[guardrails-implementation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects scope: Claude-only → use `[[claude-tool-use]]`; Gemini-only → `[[gemini-function-calling]]`; cross-vendor or OpenAI → run this methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool-registry.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/tool-registry-entry",
  "_purpose": "JSON Schema for a single tool registry entry (cross-vendor).",
  "_consumes": "operator-authored registry.json",
  "_produces": "validator verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "name",
    "version",
    "description",
    "schema_id",
    "input_schema",
    "category"
  ],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "description": {
      "type": "string",
      "minLength": 30
    },
    "schema_id": {
      "type": "string"
    },
    "input_schema": {
      "type": "object",
      "required": [
        "type",
        "properties"
      ]
    },
    "category": {
      "type": "string"
    },
    "side_effects": {
      "enum": [
        "read",
        "write",
        "external_call"
      ]
    }
  }
}
```

### `templates/agent-loop.py`

```python
"""
from __future__ import annotations

import concurrent.futures as cf
import json
from typing import Any, Callable

MAX_TURNS = 15


def run_anthropic(client, system: str, user: str, tools: list[dict], execute: Callable[[str, dict], str]) -> str:
    messages = [{"role": "user", "content": user}]
    for _ in range(MAX_TURNS):
        resp = client.messages.create(model="claude-sonnet-4-5", max_tokens=4096, system=system, tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return next((b.text for b in resp.content if b.type == "text"), "")
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        with cf.ThreadPoolExecutor() as ex:
            futures = {b.id: ex.submit(execute, b.name, b.input) for b in tool_uses}
        results = [{"type": "tool_result", "tool_use_id": bid, "content": f.result()} for bid, f in futures.items()]
        messages.append({"role": "user", "content": results})
    return "max_turns_reached"


def run_openai(client, system: str, user: str, tools: list[dict], execute: Callable[[str, dict], str]) -> str:
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for _ in range(MAX_TURNS):
        resp = client.chat.completions.create(model="gpt-4o", tools=tools, messages=messages)
        msg = resp.choices[0].message
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [tc.model_dump() for tc in (msg.tool_calls or [])]})
        if not msg.tool_calls:
            return msg.content or ""
        with cf.ThreadPoolExecutor() as ex:
            futures = {tc.id: ex.submit(execute, tc.function.name, json.loads(tc.function.arguments)) for tc in msg.tool_calls}
        for tc in msg.tool_calls:
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": futures[tc.id].result()})
    return "max_turns_reached"
```

### `templates/argument-validator.py`

```python
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    import jsonschema
except ImportError:
    jsonschema = None


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]


def validate_args(tool_entry: dict, args: dict) -> ValidationResult:
    if jsonschema is None:
        raise SystemExit("jsonschema required: pip install jsonschema")
    schema = tool_entry.get("input_schema") or {}
    errors: list[str] = []
    try:
        jsonschema.validate(instance=args, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{'.'.join(map(str, e.absolute_path))}: {e.message}")
    return ValidationResult(ok=not errors, errors=errors)


def to_tool_result(tool_call_id: str, result: ValidationResult) -> dict:
    if result.ok:
        return {"type": "tool_result", "tool_use_id": tool_call_id, "content": "OK"}
    return {"type": "tool_result", "tool_use_id": tool_call_id, "content": f"ValidationError: {'; '.join(result.errors)}", "is_error": True}
```

### `templates/tool-router.py`

```python
"""
from __future__ import annotations

from typing import Any


def select_category(query: str, categories: list[str], llm_call: Any) -> str:
    """LLM-routed: pick the single best category for the query."""
    prompt = f"Categories: {categories}\nQuery: {query}\nReply with one category name exactly."
    return llm_call(prompt).strip()


def visible_tools(registry: list[dict], category: str) -> list[dict]:
    return [t for t in registry if t.get("category") == category][:20]


def route(query: str, registry: list[dict], llm_call: Any) -> list[dict]:
    categories = sorted({t["category"] for t in registry if t.get("category")})
    cat = select_category(query, categories, llm_call)
    return visible_tools(registry, cat)
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid tool registry entry.",
  "_consumes": "validate-function-calling-patterns.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/tool-registry.schema.json",
  "_token_budget_impact": "docs-only",
  "name": "search_kb",
  "version": "1.0.0",
  "description": "Search the knowledge base for articles matching a query. Returns up to 5 results.",
  "schema_id": "kb-search-1.0",
  "category": "knowledge",
  "side_effects": "read",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string"
      }
    },
    "required": [
      "query"
    ]
  }
}
```
