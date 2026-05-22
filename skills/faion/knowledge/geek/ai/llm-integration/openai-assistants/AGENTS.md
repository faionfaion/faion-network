---
slug: openai-assistants
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Assistants API is a stateful layer over Chat Completions that manages conversation threads, file uploads, a built-in vector store (File Search), and a sandboxed Python runtime (Code Interpreter).
content_id: "5bc4d1160f015d13"
tags: [assistants-api, stateful-llm, file-search, code-interpreter, rag]
---
# OpenAI Assistants API

## Summary

**One-sentence:** The Assistants API is a stateful layer over Chat Completions that manages conversation threads, file uploads, a built-in vector store (File Search), and a sandboxed Python runtime (Code Interpreter).

**One-paragraph:** The Assistants API is a stateful layer over Chat Completions that manages conversation threads, file uploads, a built-in vector store (File Search), and a sandboxed Python runtime (Code Interpreter). It is designed for multi-turn user-facing applications where the caller should not manage message history, document indexing, or code execution infrastructure.

## Applies If (ALL must hold)

- Multi-turn user-facing applications where conversation history must persist across sessions.
- RAG over uploaded documents without building a custom vector pipeline (File Search).
- Data analysis where the LLM needs to execute Python on uploaded CSV/Excel files (Code Interpreter).
- Prototyping agent applications when stateful conversation overhead is acceptable.
- Users upload files mid-conversation and the assistant must act on them immediately.

## Skip If (ANY kills it)

- High-throughput automated pipelines — Assistants adds HTTP round-trips per turn; Chat Completions is faster.
- When deterministic, auditable tool execution is required — internal tool calling is opaque.
- Cost-sensitive workloads — file search + thread storage add per-token overhead.
- Data that must not be stored on OpenAI servers (GDPR/HIPAA) — threads and files persist.
- Sub-100ms first-token latency requirements — `create_and_poll` polling overhead is too high.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/llm-integration/`
