---
slug: feature-discovery
tier: solo
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for identifying, prioritizing, and validating product features before committing engineering effort.
content_id: "1f1a6126cc40da6e"
tags: [features, prioritization, roadmap, research, validation]
---
# Feature Discovery

## Summary

**One-sentence:** A methodology for identifying, prioritizing, and validating product features before committing engineering effort.

**One-paragraph:** A methodology for identifying, prioritizing, and validating product features before committing engineering effort. The core rule: collect feature signals from 4 sources (customer research, usage analytics, competitive analysis, market trends), classify each using the Kano model, score top candidates with RICE (Reach × Impact × Confidence / Effort), and validate the top-3 with a fake-door or prototype test before building.

## Applies If (ALL must hold)

- Pre-roadmap planning when the feature backlog has more than ~30 candidates.
- After a noticeable churn or activation drop, to decide between fixing flows and adding capability.
- When stakeholders push competing feature requests and you need a defensible ranking.
- When validating a new feature idea before committing engineering.

## Skip If (ANY kills it)

- Pre-PMF: run problem-validation first; there is no stable user base to score Reach against.
- Single-feature decisions where the cost of running RICE exceeds the cost of just building.
- Fewer than 5 features in scope — prioritization overhead exceeds value.
- Telemetry is missing — RICE on guessed Reach is theatrical.

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

- parent skill: `solo/research/researcher/`
