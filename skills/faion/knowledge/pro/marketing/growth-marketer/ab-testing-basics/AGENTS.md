---
slug: ab-testing-basics
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing (split testing) is a controlled experiment that compares two versions of a change by splitting traffic 50/50, measuring which variant performs better on a pre-registered primary metric, and deciding based on statistical significance.
content_id: "d691b648a3e4090f"
tags: [experimentation, ab-testing, split-testing, statistical-significance, hypothesis]
---
# A/B Testing Basics

## Summary

**One-sentence:** A/B testing (split testing) is a controlled experiment that compares two versions of a change by splitting traffic 50/50, measuring which variant performs better on a pre-registered primary metric, and deciding based on statistical significance.

**One-paragraph:** A/B testing (split testing) is a controlled experiment that compares two versions of a change by splitting traffic 50/50, measuring which variant performs better on a pre-registered primary metric, and deciding based on statistical significance. The lifecycle is: hypothesis (if/then/because) → sample-size calculation → run to full size → analyze (p-value, SRM check, guardrails) → ship or kill.

## Applies If (ALL must hold)

- Reversible UI/copy/flow changes where the change affects a metric trackable in real time.
- At least 1k weekly events on the primary metric surface.
- One change per experiment — multiple simultaneous changes prevent causal isolation.
- Team has committed to a single primary metric and 3+ guardrail metrics before launch.
- A/B platform available with deterministic-hash bucketing (user_id + experiment_id).

## Skip If (ANY kills it)

- Strategic choices (pricing model, brand positioning) — blast radius too large, too few decisions.
- Network-effect surfaces (Slack workspaces, marketplaces) — treatment leaks into control; use cluster/switchback designs.
- Traffic below 100 users/day on the test surface — test duration exceeds product-iteration cadence.
- Full redesigns — too many confounders; use phased feature-flag rollout instead.
- Highly personalized products where every user already sees a different variant.

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
