---
slug: manifest-then-fetch
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A tool-result protocol where every tool returns a small manifest first (execution_id, preview, size_tokens) and the full payload is stored externally.
content_id: "3e6c69a2cee7b855"
tags: [tool-calling, context-management, agent-protocol, lazy-loading, manifest]
---
# Manifest-Then-Fetch — Two-Phase Tool Result

## Summary

**One-sentence:** A tool-result protocol where every tool returns a small manifest first (execution_id, preview, size_tokens) and the full payload is stored externally.

**One-paragraph:** A tool-result protocol where every tool returns a small manifest first (execution_id, preview, size_tokens) and the full payload is stored externally. The agent inspects only the preview; it must explicitly call get_full_result(execution_id) to load the body. Default behaviour is preview-only — large payloads never enter the LLM context unless the agent decides they are needed.

## Applies If (ALL must hold)

- Tools with high payload variance — web_fetch, sql_query, log_search, read_file on unknown sizes.
- Agents that loop ≥30 turns and accumulate tool history.
- Pipelines where most calls only need a count, header, or first match.
- Multi-tenant agent platforms where some tools occasionally return megabyte responses.

## Skip If (ANY kills it)

- Tools where every result is small (<1k tokens) — the manifest dance is pure overhead.
- Single-shot stateless tool calls in a one-turn agent — no later step exists to fetch the body.
- Streaming tools where the agent must act on each chunk live — manifests delay action.

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

- parent skill: `geek/ai/ai-agents/`
