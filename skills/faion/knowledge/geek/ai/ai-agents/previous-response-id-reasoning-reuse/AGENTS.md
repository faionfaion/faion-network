---
slug: previous-response-id-reasoning-reuse
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When chaining turns of an OpenAI reasoning model (o3, o4-mini, gpt-5) on the Responses API, pass previous_response_id=<prior.
content_id: "fa50821543b6ae75"
tags: [reasoning, responses-api, agent-continuity, cache-optimization, multi-turn]
---
# previous_response_id — Reasoning-Item Reuse on the Responses API

## Summary

**One-sentence:** When chaining turns of an OpenAI reasoning model (o3, o4-mini, gpt-5) on the Responses API, pass previous_response_id=<prior.

**One-paragraph:** When chaining turns of an OpenAI reasoning model (o3, o4-mini, gpt-5) on the Responses API, pass previous_response_id=<prior.id> instead of reconstructing a Chat-Completions–style message array. The Responses API keeps reasoning items adjacent to their function calls server-side, keyed by id; supplying the id reattaches them on the next turn. This preserves the model's mid-loop "thinking", lifts cache-hit rate, and cuts both latency and tokens. Under ZDR (store=false), use the encrypted-content variant instead — previous_response_id is silently ignored.

## Applies If (ALL must hold)

- Multi-turn agent loops on o3, o4-mini, or gpt-5 where the model calls tools and you feed results back.
- Conversational reasoning agents where consecutive user turns continue the same task.
- Long planning loops where mid-trajectory thoughts inform later decisions.
- Anywhere you previously paid for "re-thinking" by reconstructing message arrays manually.

## Skip If (ANY kills it)

- Non-reasoning models (gpt-4.1, gpt-4.1-mini) — there are no reasoning items to reuse.
- ZDR / store=false deployments — the id is silently ignored; use include=["reasoning.encrypted_content"] and round-trip the blob (see encrypted-reasoning pattern).
- First turn of a session — there is no prior id yet; pass the user message normally.
- Cross-session continuation — reasoning items expire; do not assume yesterday's id still resolves.

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
