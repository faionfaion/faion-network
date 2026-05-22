---
slug: ollama-python-client
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Ollama exposes a REST API at http://localhost:11434 and an official Python library (pip install ollama).
content_id: "bcc4fbb3c568a1f5"
tags: [ollama, python, async, streaming]
---
# Ollama Python Client Patterns

## Summary

**One-sentence:** Ollama exposes a REST API at http://localhost:11434 and an official Python library (pip install ollama).

**One-paragraph:** Ollama exposes a REST API at http://localhost:11434 and an official Python library (pip install ollama). This methodology covers sync and async integration patterns, streaming responses, embeddings, vision models, and a production-ready service class with retry logic and metrics.

## Applies If (ALL must hold)

- Building a Python application that calls a local Ollama instance.
- Needing concurrent batch processing with asyncio.
- Requiring streaming output for real-time UX.
- Generating embeddings locally for RAG pipelines.
- Processing images with local vision models.

## Skip If (ANY kills it)

- Production cloud deployment where OpenAI SDK with Ollama base_url override suffices — see ollama-agent-integration.
- Simple one-off scripting where the CLI (ollama run) is faster to use.
- TypeScript/JavaScript frontends — use the OpenAI-compatible REST API directly.

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

- parent skill: `geek/ai/ml-engineer/`
