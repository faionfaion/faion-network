# Gemini Function Calling

## Summary

Gemini function calling lets Python functions serve as LLM tools by using their docstrings and type hints as the tool schema. The SDK supports automatic mode (model executes tools in-process) and manual mode (caller controls execution). Beyond tools, Gemini offers Google Search grounding for live web data and `text-embedding-004` (768-dim) for RAG pipelines, plus native JSON schema-constrained output via `response_mime_type`.

## Why

Gemini is the preferred choice when the pipeline is already on Google Cloud / Vertex AI, when Google Search grounding is required (live news, prices, current events), or when embedding generation with `text-embedding-004` feeds a Qdrant/Chroma index. It removes the need to write JSON tool schemas manually — Python docstrings become the schema automatically. For structured extraction, `response_mime_type="application/json"` is available on all 1.5+ models without function-forcing.

## When To Use

- Pipelines running on Google Cloud / Vertex AI infrastructure.
- Tasks requiring Google Search grounding for live web data.
- RAG pipelines using `text-embedding-004` (768-dim, multilingual).
- Structured extraction with JSON schema (simpler than tool-forcing).
- Agent loops where automatic function calling simplifies the orchestrator.

## When NOT To Use

- OpenAI or Claude is already in the pipeline — adding Gemini increases vendor surface area without clear benefit unless Search grounding is needed.
- Production pipelines requiring deterministic, auditable tool execution — use manual mode, not automatic.
- Tasks requiring Anthropic Extended Thinking-level transparent reasoning.
- Complex nested function signatures — Gemini parses docstrings as schema; complex types degrade accuracy.

## Content

| File | What's inside |
|------|---------------|
| `content/01-function-calling.xml` | Manual vs. automatic modes, tool config, parallel calling rules, gotchas. |
| `content/02-grounding-embeddings.xml` | Search grounding setup, dynamic threshold tuning, embedding task types, cosine similarity. |

## Templates

| File | Purpose |
|------|---------|
| `templates/manual-tool-call.py` | Auditable manual function calling pattern with validation. |
| `templates/structured-extraction.py` | JSON schema extraction via response_mime_type (no tool use). |
| `templates/embed-batch.py` | Batch embedding helper with task type selection. |
