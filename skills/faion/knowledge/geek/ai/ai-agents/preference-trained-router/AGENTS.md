---
slug: preference-trained-router
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Train a tiny router (matrix factorization, BERT classifier, or similarity ranker) on Chatbot-Arena-style preference data so it can decide BEFORE inference whether each prompt should go to the weak or strong model.
content_id: "42cc5450114cb88e"
tags: [routing, cost-optimization, model-selection, preference-learning, routellm]
---
# Preference-Trained Router (RouteLLM Pattern)

## Summary

**One-sentence:** Train a tiny router (matrix factorization, BERT classifier, or similarity ranker) on Chatbot-Arena-style preference data so it can decide BEFORE inference whether each prompt should go to the weak or strong model.

**One-paragraph:** Train a tiny router (matrix factorization, BERT classifier, or similarity ranker) on Chatbot-Arena-style preference data so it can decide BEFORE inference whether each prompt should go to the weak or strong model. One round-trip, one decision, no cascade. The router is a learned binary classifier on the prompt embedding, not a heuristic — and it must be retrained when traffic distribution drifts.

## Applies If (ALL must hold)

- Latency-sensitive production traffic where the cascade round-trip is unacceptable.
- You have ≥10k logged (prompt, weak-output, strong-output) tuples to train on (or can use Arena public data + a few thousand of your own).
- Mostly-stable task distribution — router quality decays under distribution shift.
- Token spend on the strong model is the dominant line item AND the workload mixes easy and hard prompts.

## Skip If (ANY kills it)

- Cold start with no preference data — train a cascade first, log Arena pairs, switch later.
- Rapidly drifting traffic (new product, weekly feature changes) — the router goes stale faster than you can retrain it.
- Adversarial or safety-critical paths where a wrong-but-confident route is unacceptable; use a cascade with explicit verification instead.
- Single-model workloads where the strong model's marginal cost is already low (small prompts, cached prefix).

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
