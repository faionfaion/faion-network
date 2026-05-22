---
slug: reasoning-first-architectures
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for using reasoning models (o3/o4-mini, Claude Extended Thinking, DeepSeek R1) and chain-of-thought techniques to solve tasks requiring multi-step logic, self-verification, and planning.
content_id: "69084dee94f28ecc"
tags: [reasoning-models, chain-of-thought, extended-thinking, cost-optimization, agentic-workflow]
---
# Reasoning-First Architectures

## Summary

**One-sentence:** Patterns for using reasoning models (o3/o4-mini, Claude Extended Thinking, DeepSeek R1) and chain-of-thought techniques to solve tasks requiring multi-step logic, self-verification, and planning.

**One-paragraph:** Patterns for using reasoning models (o3/o4-mini, Claude Extended Thinking, DeepSeek R1) and chain-of-thought techniques to solve tasks requiring multi-step logic, self-verification, and planning. Route by task complexity: use cheap classifiers to decide when a reasoning model is warranted, set thinking budgets explicitly, and always gate irreversible downstream actions behind human review.

## Applies If (ALL must hold)

- Multi-step math, logic, or formal proofs where intermediate steps matter
- Code generation requiring self-verification before returning
- Research synthesis where competing hypotheses must be explored before concluding
- Planning tasks with dependencies where ordering must be validated
- Any workflow where the cost of a wrong answer outweighs the cost of extra tokens

## Skip If (ANY kills it)

- Simple retrieval or lookup tasks — CoT adds latency with no quality gain
- High-throughput classification or routing (thousands of calls per minute)
- Creative writing where deliberate reasoning constrains output quality
- Cost-sensitive pipelines where standard models already meet the bar (verified by eval)
- Real-time streaming where users see partial output — reasoning tokens break UX

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
