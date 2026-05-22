---
slug: feature-prioritization-rice
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Quantitative scoring model that ranks features by `(Reach × Impact × Confidence) / Effort`.
content_id: "ed007ef10322796b"
tags: [prioritization, rice, product-ops, scoring, roadmap]
---
# Feature Prioritization (RICE)

## Summary

**One-sentence:** Quantitative scoring model that ranks features by `(Reach × Impact × Confidence) / Effort`.

**One-paragraph:** Quantitative scoring model that ranks features by `(Reach × Impact × Confidence) / Effort`. Reach is users per quarter from analytics; Impact uses a fixed 5-point scale (3/2/1/0.5/0.25); Confidence is capped at 50% without cited evidence; Effort is total person-months including design, dev, QA, and docs. Higher score = higher priority. Re-score quarterly; archive prior scoring files with date stamps.

## Applies If (ALL must hold)

- Backlog has 10+ candidates needing an objective, repeatable rank for the next quarter or release.
- Stakeholders disagree on priority and you need a math-based artifact to defuse HiPPO.
- A subagent drafts a roadmap from a raw idea list and needs a defensible default ordering.
- You have at least funnel/MAU data plus an effort estimate per item.

## Skip If (ANY kills it)

- Single-feature decisions — RICE adds noise versus a one-liner rationale.
- Pre-PMF / 0-to-1 products where Reach is unknowable — use opportunity solution trees or Kano.
- Compliance, security, or contractual must-haves — they bypass RICE and go straight into the plan.
- Cross-portfolio bets where strategic fit dominates the score (RICE has no strategy term).

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

- parent skill: `solo/product/product-operations/`
