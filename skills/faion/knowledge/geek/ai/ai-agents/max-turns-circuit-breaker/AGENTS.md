---
slug: max-turns-circuit-breaker
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Set an explicit max_turns on every production agent run (5-10 for retrieval, 15-20 for coding agents) and CATCH the resulting MaxTurnsExceeded exception.
content_id: "7a38dbac4a8f6ed2"
tags: [agent-patterns, resilience, error-handling, production-deployment, cost-control]
---
# Max-Turns as Circuit Breaker, Not Error

## Summary

**One-sentence:** Set an explicit max_turns on every production agent run (5-10 for retrieval, 15-20 for coding agents) and CATCH the resulting MaxTurnsExceeded exception.

**One-paragraph:** Set an explicit max_turns on every production agent run (5-10 for retrieval, 15-20 for coding agents) and CATCH the resulting MaxTurnsExceeded exception. On catch, hand the partial trajectory to a cheap recovery model that summarizes what was tried and asks the user to clarify, instead of bubbling a 500. Hard turn caps are the only deterministic stop for tool-calling loops that fail by silently consuming budget.

## Applies If (ALL must hold)

- Every Runner.run / agent-loop invocation that calls tools.
- Retrieval agents (cap 5-10 turns) and code-editing agents (cap 15-20).
- Production deployments where budget is finite and silent loops drain credit.
- Multi-tenant SaaS where one stuck loop can starve others of rate-limit headroom.

## Skip If (ANY kills it)

- Long-running async coding agents in sandboxes designed for hundreds of turns — use checkpoint + human approval instead, not a single max-turns.
- Chat completions with no tool use — the model already terminates on first non-tool reply.
- Workflows where the cap is an unrecoverable error (DB transaction half-applied) — solve with idempotency, not a turn cap.

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
