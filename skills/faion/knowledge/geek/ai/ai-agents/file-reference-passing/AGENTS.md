---
slug: file-reference-passing
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When agent step N analyzes a corpus, return only references (file paths, IDs, URLs, doc-keys) — not the content itself.
content_id: "45e2e86e13d09a95"
tags: [pipeline, context-economy, references, lazy-loading, multi-stage]
---
# File-Reference Passing Between Pipeline Steps

## Summary

**One-sentence:** When agent step N analyzes a corpus, return only references (file paths, IDs, URLs, doc-keys) — not the content itself.

**One-paragraph:** When agent step N analyzes a corpus, return only references (file paths, IDs, URLs, doc-keys) — not the content itself. Step N+1 loads from those references on demand. The corollary: the boundary between agent steps is a list of POINTERS, not a payload of CONTENT.

## Applies If (ALL must hold)

- Multi-stage pipelines where each stage operates on a corpus
- Map-reduce patterns over documents
- Agents with subagents (subagent returns a slim summary + refs; parent re-fetches if needed)
- Long documents where only some passages matter to downstream
- Any time you find yourself ferrying > 2K tokens of "context" between steps

## Skip If (ANY kills it)

- Single-shot agents (no downstream step exists)
- When the content is small enough that lazy-loading adds more overhead than it saves
- When refs are unstable (URLs that expire, IDs that get reassigned) — use snapshotted refs
- When the downstream model lacks tools to load by ref (no file-read tool, no DB-fetch tool)

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
