---
slug: ab-testing-setup
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing setup covers the technical and analytical groundwork for a valid experiment: accurate sample-size calculation (statsmodels NormalIndPower, not the simplified 16×p(1-p)/MDE² teaching formula), traffic-split configuration with deterministic-hash bucketing, SRM monitoring from day 1, and a plan-and-results template that an analyst agent fills in deterministically.
content_id: "09b23bc4d257e097"
tags: [ab-testing, experimentation, sample-size, statistical-power, experiment-design]
---
# A/B Testing Setup

## Summary

**One-sentence:** A/B testing setup covers the technical and analytical groundwork for a valid experiment: accurate sample-size calculation (statsmodels NormalIndPower, not the simplified 16×p(1-p)/MDE² teaching formula), traffic-split configuration with deterministic-hash bucketing, SRM monitoring from day 1, and a plan-and-results template that an analyst agent fills in deterministically.

**One-paragraph:** A/B testing setup covers the technical and analytical groundwork for a valid experiment: accurate sample-size calculation (statsmodels NormalIndPower, not the simplified 16×p(1-p)/MDE² teaching formula), traffic-split configuration with deterministic-hash bucketing, SRM monitoring from day 1, and a plan-and-results template that an analyst agent fills in deterministically.

## Applies If (ALL must hold)

- Pre-launch sample-size and duration calculation for any planned experiment.
- Configuring traffic split, randomization, and SRM monitoring in Statsig, GrowthBook, LaunchDarkly, or equivalent.
- Auditing a draft test plan against the pre-launch checklist before traffic flows.
- Generating plan and results templates that analysts fill in consistently across the team.

## Skip If (ANY kills it)

- Network-effect surfaces (chat, marketplace, multiplayer) — independent randomization is invalid; use cluster or switchback designs.
- Heavy personalization where every user already sees a unique variant — plain A/B math doesn't apply.
- Single-shot critical decisions (pricing model, brand direction) — blast radius too large.
- Pre-instrumentation: if the primary metric is not tracked end-to-end yet, instrument first; computing sample size is meaningless otherwise.
- Continuous heavy-tailed outcome metrics (revenue per user) without log-transform or bootstrap — proportion math misleads.

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

- parent skill: `pro/marketing/growth-marketer/`
