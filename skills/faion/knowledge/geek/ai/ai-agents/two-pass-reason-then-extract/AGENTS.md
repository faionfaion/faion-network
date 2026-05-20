---
slug: two-pass-reason-then-extract
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When raw reasoning quality matters more than output format (math proofs, deep research synthesis, code with subtle constraints), do not lock the strong model into strict JSON during the reasoning step.
content_id: "73f431bab75696ea"
tags: [reasoning, structured-output, cost-optimization, model-cascade]
---
# Two-Pass: Free-Form Reasoning Then Structured Extraction

## Summary

**One-sentence:** When raw reasoning quality matters more than output format (math proofs, deep research synthesis, code with subtle constraints), do not lock the strong model into strict JSON during the reasoning step.

**One-paragraph:** When raw reasoning quality matters more than output format (math proofs, deep research synthesis, code with subtle constraints), do not lock the strong model into strict JSON during the reasoning step. Run two passes: (1) the strong model reasons in free text or extended-thinking mode, (2) a cheap small model extracts the answer into the strict schema. The format constraint never interferes with the reasoning trace, and the strict typing still lands on the consumer.

## Applies If (ALL must hold)

- Math word problems, proofs, multi-step calculations.
- Research synthesis where the answer is a few fields but the analysis is paragraphs.
- Code generation that needs deep reasoning before a structured diff/patch.
- Legal or medical analysis where the verdict structure is rigid but the reasoning must be unconstrained.
- Anything where Opus extended thinking is justified by the task difficulty.

## Skip If (ANY kills it)

- Simple extraction (entities, key/value, sentiment) — single-pass strict SO is faster and cheaper.
- Latency-critical paths under ~1 second total — two model calls always cost more wall-clock than one.
- Tasks small enough that Haiku-class extraction quality is the bottleneck — extract directly with the strong model.
- High call volume where the doubled provider cost exceeds the accuracy gain.

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
