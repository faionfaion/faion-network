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

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-basics.py` | Validates gemini-config-basic.json: pinned model + temperature + max_output_tokens. | Pre-commit on starter config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-api-integration]]`
- `[[gemini-function-calling]]`
- `[[gemini-multimodal]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` routes the call: function-calling or multimodal needs route to siblings; basic text/chat routes here.
