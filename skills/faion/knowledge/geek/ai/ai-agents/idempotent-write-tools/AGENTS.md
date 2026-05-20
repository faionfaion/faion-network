---
slug: idempotent-write-tools
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every tool that mutates state must accept an idempotency_key from the agent and be safe to re-run with the same key (returns the same result without duplicating the side effect).
content_id: "14a51dbde469ddc0"
tags: [idempotency, tooling, agents, reliability, safety]
---
# Idempotent Write Tools — Keys + Preview/Apply Pairs

## Summary

**One-sentence:** Every tool that mutates state must accept an idempotency_key from the agent and be safe to re-run with the same key (returns the same result without duplicating the side effect).

**One-paragraph:** Every tool that mutates state must accept an idempotency_key from the agent and be safe to re-run with the same key (returns the same result without duplicating the side effect). Destructive or expensive operations ship as *_preview + *_apply pairs, separating the agent's reasoning step from the irreversible commit step. Tools time out, networks flake, agent loops retry on transient errors — un-keyed writes silently double-charge, double-deploy, double-email. Idempotency keys turn every retry into a no-op replay; preview/apply pairs let the agent show its work before committing.

## Applies If (ALL must hold)

- Any tool that mutates external state: payments, emails, file deletes, infra changes, DB writes, external API POSTs.
- Tools whose side effect is destructive (delete) or expensive (deploy, send email, charge card) — split into *_preview + *_apply.
- When the agent runs in a loop with automatic retry on tool errors.
- When tools are exposed via MCP gateways with at-least-once delivery semantics.

## Skip If (ANY kills it)

- Pure reads (get_*, search_*, list_*) — no side effect, no key needed; bloating the schema confuses the model.
- Append-only telemetry where duplicates are tolerable (metric emits, debug logs).
- Tools whose underlying API is already idempotent by content hash (e.g., S3 PUT with same body) — passing a key adds noise.

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
