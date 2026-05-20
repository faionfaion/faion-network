---
slug: feature-prioritization-rice
tier: solo
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Score each candidate feature as (Reach x Impact x Confidence) / Effort.
content_id: "ed007ef10322796b"
tags: [prioritization, rice, scoring, roadmap, feature-ranking]
---
# Feature Prioritization (RICE)

## Summary

**One-sentence:** Score each candidate feature as (Reach x Impact x Confidence) / Effort.

**One-paragraph:** Score each candidate feature as (Reach x Impact x Confidence) / Effort. Reach = users affected per quarter (cite an analytics query or proxy metric). Impact = {3, 2, 1, 0.5, 0.25} only — do not add intermediate values. Confidence = 100%/80%/50% only — drop one tier for each unknown. Effort = person-months including design, dev, QA, and a 30% buffer for unknowns; engineers must own this column. Sort highest-to-lowest, sanity-check, then apply strategic veto for one bet that may rank lower but is the only path to differentiation.

## Applies If (ALL must hold)

- Comparing 5+ candidate features in a single quarter where reach and effort vary widely.
- Killing pet features: a numeric score forces debate on inputs, not opinions.
- Triaging a backlog after a discovery sprint produced more validated problems than capacity.
- Deciding between two features that both look "obviously valuable" — RICE exposes effort-adjusted ROI.

## Skip If (ANY kills it)

- Solo founder with fewer than 3 candidates — overhead exceeds signal; pick by gut and ship.
- Hard-deadline regulatory or compliance work — there is no score; you ship or get fined.
- Discovery phase before reach and impact data exist — confidence will be 50% across the board and ranking is noise.
- Strategic bets / 0-to-1 features — RICE punishes high-effort items even when they are the only path to a moat.

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

- parent skill: `solo/product/product-manager/`
