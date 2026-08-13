# Gemini Function Calling

## Summary

**One-sentence:** Produces a Gemini function-calling integration — Python function declarations via docstring + types, manual-mode loop, JSON-schema response, optional Search grounding.

**One-paragraph:** Gemini exposes Python functions as tools via docstring + type hints; SDK derives the schema automatically. Two execution modes: automatic (SDK runs the function in-process) and manual (caller dispatches). For production, prefer manual mode for auditability + scope enforcement. Beyond tool use, response_mime_type="application/json" + response_schema delivers schema-constrained typed output without forcing a tool. Google Search grounding is available behind a `tools=[Tool(google_search=...)]` flag and doubles per-query cost.

**Ефективно для:** RAG-adjacent retrieval pipelines, agent loops on Gemini, schema-constrained extraction, live-search agents.

## Applies If (ALL must hold)

- Vendor is Gemini (cost or capability reason).
- Tool count ≤ 20 OR a router upstream.
- Python signatures with type hints; no exotic nested types.
- Caller can wrap the SDK manual-mode loop.

## Skip If (ANY kills it)

- Single-vendor stack on Anthropic / OpenAI — use the respective methodology.
- Need streaming-with-tool-calls — Gemini support is limited; non-streaming preferred.
- Auto-mode used to "save code" — auto is fine for prototypes, not production.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool registry | Python functions | application code |
| Gemini SDK + key | secret | secrets manager |
| Output schema (if JSON) | JSON Schema or pydantic | spec |
| Search grounding budget | doc | finops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[gemini-api-integration]]` | Safety + Files API baseline. |
| `[[function-calling-patterns]]` | Cross-vendor router + validation patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: docstring required, type hints required, manual mode in prod, validate args before exec, ≤20 tools, JSON via response_schema | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for gemini-tool-decl + function-response shape | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: auto-mode in prod, docstringless functions, nested types, grounding-always-on, no validation | ~600 |
| `content/04-procedure.xml` | medium | 6-step: declare functions → set mode → wire loop → enable grounding selectively → handle JSON → eval | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "vendor=Gemini AND tool use needed?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Write function docstrings | sonnet | Pattern code. |
| Implement manual loop | sonnet | Mechanical. |
| Decide grounding budget | opus | Cost reasoning. |
| Tune response_schema | sonnet | Schema authoring. |

## Templates

| File | Purpose |
|---|---|
| `templates/gemini-fc-client.py` | Manual-mode function-calling loop reference. |
| `templates/function-declaration-example.py` | Function with docstring + type hints producing a tool. |
| `templates/_smoke-test.json` | Minimum valid gemini-fc config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-function-calling.py` | Validates gemini-fc config: mode + tool count ≤20 + response_schema if JSON. | Pre-commit on config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-api-integration]]`
- `[[function-calling-patterns]]`
- `[[claude-tool-use]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` routes: non-Gemini → skip; Gemini + ≤20 tools + manual mode acceptable → run-the-checklist.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/gemini-fc-client.py`

```python
"""
from __future__ import annotations

import json
from typing import Callable

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

MAX_TURNS = 15


def run_manual_fc(client, model: str, system: str, user: str, tools: list[Callable], validators: dict[str, Callable]) -> str:
    """Manual-mode loop: caller dispatches the LLM-requested tool."""
    if types is None:
        raise SystemExit("google-genai required")
    chat = client.chats.create(model=model, config=types.GenerateContentConfig(system_instruction=system, tools=tools))
    msg = user
    for _ in range(MAX_TURNS):
        resp = chat.send_message(msg)
        if not resp.function_calls:
            return resp.text
        msg = []
        for fc in resp.function_calls:
            validator = validators.get(fc.name)
            args = dict(fc.args)
            if validator and not validator(args):
                msg.append(types.Part.from_function_response(name=fc.name, response={"error": "validation_failed"}))
                continue
            fn = next((t for t in tools if t.__name__ == fc.name), None)
            if not fn:
                msg.append(types.Part.from_function_response(name=fc.name, response={"error": "unknown_function"}))
                continue
            result = fn(**args)
            msg.append(types.Part.from_function_response(name=fc.name, response={"result": result}))
    return "max_turns_reached"
```

### `templates/function-declaration-example.py`

```python
"""
from __future__ import annotations


def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location.

    Args:
        location: City name with optional country (e.g. "Kyiv, UA").
        unit: Temperature unit; "celsius" or "fahrenheit". Defaults to celsius.

    Returns:
        Dict with keys: temperature (number), conditions (string), humidity (number).
    """
    # Real implementation calls a weather API; placeholder for illustration.
    return {"temperature": 18.5, "conditions": "Cloudy", "humidity": 70}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid gemini-fc-config.",
  "_consumes": "validate-gemini-function-calling.py",
  "_produces": "ok verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "docs-only",
  "mode": "manual",
  "tools": [
    {
      "name": "search_kb",
      "description": "Search the knowledge base; returns top five matches by relevance."
    },
    {
      "name": "get_user",
      "description": "Fetch a user profile object by stable user_id from the auth service."
    }
  ],
  "search_grounding": false
}
```
