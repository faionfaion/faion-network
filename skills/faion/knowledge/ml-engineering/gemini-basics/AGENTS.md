# Gemini Basics

## Summary

**One-sentence:** Produces a starter Gemini text/chat integration — SDK init, model pick (Flash vs Pro), single-shot generate, streaming, multi-turn chat, JSON response mode.

**One-paragraph:** This methodology provides the minimum-viable starting point for a new Gemini integration: client init with API key or Vertex creds, text-only generate_content for one-shot calls, generate_content_stream for streaming, chat sessions for multi-turn, and response_mime_type="application/json" for typed output. Skip when function calling, multimodal, or Files API is needed — those are sibling methodologies.

**Ефективно для:** prototypes, classification, summarisation, chat features, JSON extraction at small scale.

## Applies If (ALL must hold)

- New Gemini integration; no function calling or multimodal needed yet.
- Single-process app; no Vertex Cloud-scale plumbing needed yet.
- Caller can handle async / streaming if used.
- Cost budget allows experimenting.

## Skip If (ANY kills it)

- Function calling required → `[[gemini-function-calling]]`.
- Multimodal (audio/image/video) → `[[gemini-multimodal]]`.
- Large file uploads / Vertex enterprise → `[[gemini-api-integration]]`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API key or Vertex creds | secret | env var |
| Use-case description | doc | spec |
| Sample input/output pair | text | eval set |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[gemini-api-integration]]` | Sibling for the safety/Files-API extensions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: explicit model, no env-key leak, streaming-or-not commit, JSON via mime_type, chat history bounded | ~600 |
| `content/02-output-contract.xml` | essential | Minimum gemini-config-basic.json schema | ~500 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: hard-coded key, model not pinned, stream-and-await mix, JSON-string-output, unbounded chat history | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "starter call, no function/multimodal/Vertex needed?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pick model | sonnet | Cost/quality. |
| Wire streaming | runtime | Mechanical. |
| Bound chat history | runtime | Mechanical. |

## Templates

| File | Purpose |
|---|---|
| `templates/gemini-basic-client.py` | Reference Python client (one-shot + streaming + chat). |
| `templates/gemini-config-basic.schema.json` | JSON Schema for starter config. |
| `templates/_smoke-test.json` | Minimum valid starter config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-basics.py` | Validates gemini-config-basic.json: pinned model + temperature + max_output_tokens. | Pre-commit on starter config. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-api-integration]]`
- `[[gemini-function-calling]]`
- `[[gemini-multimodal]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` routes the call: function-calling or multimodal needs route to siblings; basic text/chat routes here.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/gemini-basic-client.py`

```python
"""
from __future__ import annotations

import os

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def make_client():
    if genai is None:
        raise SystemExit("google-genai required: pip install google-genai")
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def generate_once(client, cfg: dict, prompt: str) -> str:
    resp = client.models.generate_content(
        model=cfg["model"],
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=cfg["temperature"],
            max_output_tokens=cfg["max_output_tokens"],
            response_mime_type=cfg.get("response_mime_type", "text/plain"),
        ),
    )
    return resp.text


def stream(client, cfg: dict, prompt: str):
    for chunk in client.models.generate_content_stream(
        model=cfg["model"],
        contents=prompt,
        config=types.GenerateContentConfig(temperature=cfg["temperature"], max_output_tokens=cfg["max_output_tokens"]),
    ):
        yield chunk.text


def chat_session(client, cfg: dict, history_cap_chars: int = 60000):
    chat = client.chats.create(model=cfg["model"])

    def send(message: str) -> str:
        resp = chat.send_message(message)
        # Trim history to budget (FIFO).
        while sum(len(h.parts[0].text) for h in chat.get_history()) > history_cap_chars:
            chat.get_history().pop(0)
        return resp.text

    return send
```

### `templates/gemini-config-basic.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/gemini-config-basic",
  "_purpose": "JSON Schema for starter Gemini config.",
  "_consumes": "operator-authored config",
  "_produces": "validator verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "model",
    "temperature",
    "max_output_tokens"
  ],
  "properties": {
    "model": {
      "type": "string",
      "pattern": "^gemini-"
    },
    "temperature": {
      "type": "number",
      "minimum": 0,
      "maximum": 2
    },
    "max_output_tokens": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65536
    },
    "response_mime_type": {
      "enum": [
        "text/plain",
        "application/json"
      ]
    },
    "streaming": {
      "type": "boolean"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid starter gemini-config-basic.",
  "_consumes": "validate-gemini-basics.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/gemini-config-basic.schema.json",
  "_token_budget_impact": "docs-only",
  "model": "gemini-2.5-flash",
  "temperature": 0.3,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
  "streaming": false
}
```
