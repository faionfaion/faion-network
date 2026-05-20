---
slug: ab-testing-basics
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing compares two or more variants of a feature using deterministic hash-based assignment to measure which performs better on a pre-registered primary metric.
content_id: "d691b648a3e4090f"
tags: [a-b-testing, experimentation, experimental-design, statistical-testing, variant-assignment]
---
# A/B Testing Basics

## Summary

**One-sentence:** A/B testing compares two or more variants of a feature using deterministic hash-based assignment to measure which performs better on a pre-registered primary metric.

**One-paragraph:** A/B testing compares two or more variants of a feature using deterministic hash-based assignment to measure which performs better on a pre-registered primary metric. Define an Experiment (hypothesis, variants, metrics, target sample size) before writing any code; bucket users with hash(experiment_id + user_id) % 10000 for stable, reproducible assignments.

## Applies If (ALL must hold)

- Testing UI/UX changes (button text, layout, checkout flow) before full rollout.
- Evaluating algorithm improvements (search ranking, recommendation) with a defined success metric.
- Pricing or copy experiments where conversion delta is the primary signal.
- Any change where you need a causal (not correlational) lift estimate.

## Skip If (ANY kills it)

- Rollouts where randomization is impossible (e.g., infrastructure changes) — use quasi-experimental methods.
- Multi-armed bandit / adaptive allocation — this methodology is fixed-split only.
- High-throughput platforms with thousands of concurrent experiments — use a managed platform (Statsig, Optimizely, GrowthBook) instead of the code snippets here.
- When you cannot reach the required sample size — switch to qualitative research.

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

- parent skill: `solo/dev/automation-tooling/`
