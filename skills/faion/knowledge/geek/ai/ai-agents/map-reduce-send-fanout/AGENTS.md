---
slug: map-reduce-send-fanout
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use dynamic fan-out (Send(node, payload) in LangGraph, ParallelAgent in ADK, asyncio.
content_id: "5297a6c211347021"
tags: [parallelization, langgraph, fan-out, concurrency, map-reduce]
---
# Map-Reduce Fan-Out with Bounded Concurrency and Idempotent Branches

## Summary

**One-sentence:** Use dynamic fan-out (Send(node, payload) in LangGraph, ParallelAgent in ADK, asyncio.

**One-paragraph:** Use dynamic fan-out (Send(node, payload) in LangGraph, ParallelAgent in ADK, asyncio.gather in plain Python) to map a per-item LLM call across a list, then reduce with an annotated reducer (Annotated[list, operator.add] or a custom merge). Cap concurrency at ≤20 to avoid rate-limit cliffs, and design every branch to be idempotent + retryable because any single branch failure fails the entire super-step atomically. Never use map-reduce fan-out for branches that mutate shared external state — use a queue + workers instead.

## Applies If (ALL must hold)

- Per-document scoring or classification across N documents.
- Multi-source RAG fan-out (vector search + web search + memory lookup, then merge).
- Multi-candidate generation (sample N drafts, pick best with a reducer / vote).
- Batch tool calls over a list (enrich N rows, classify N emails) where each item is independent.

## Skip If (ANY kills it)

- Fixed-N parallel where N is known at graph-compile time — use static fan-out edges; Send is for runtime-variable N.
- Branches that mutate shared external state (write to the same DB row, append to one file) — use a queue + workers, not Send. Atomic-fail of the super-step double-applies on retry.
- N > 20 with a single provider — split into batches, otherwise rate-limit kills the run; or move to provider Batch API.
- Strong consistency requirements across branches (every branch must see the same prior state) — use sequential.

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
