---
slug: gemini-function-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Gemini function-calling integration — Python function declarations via docstring + types, manual-mode loop, JSON-schema response, optional Search grounding.
content_id: "02ab428132bc6fef"
complexity: medium
produces: code
est_tokens: 3000
tags: [gemini, function-calling, grounding, embeddings, structured-output]
---
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
