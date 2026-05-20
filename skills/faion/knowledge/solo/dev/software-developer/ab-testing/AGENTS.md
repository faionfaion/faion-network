---
slug: ab-testing
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing runtime implementation covering deterministic variant assignment, exposure and conversion event tracking, statistical analysis (z-test for proportions, Wilson CI), and Sample Ratio Mismatch detection.
content_id: "b7f4b22564934e1d"
tags: [a-b-testing, experimentation, statistics, feature-flags, hypothesis-testing]
---
# A/B Testing Implementation

## Summary

**One-sentence:** A/B testing runtime implementation covering deterministic variant assignment, exposure and conversion event tracking, statistical analysis (z-test for proportions, Wilson CI), and Sample Ratio Mismatch detection.

**One-paragraph:** A/B testing runtime implementation covering deterministic variant assignment, exposure and conversion event tracking, statistical analysis (z-test for proportions, Wilson CI), and Sample Ratio Mismatch detection. Core rule: assignment must use deterministic hashing (hash(user_id || experiment_id) mod 100) — never random.choice — to ensure sticky bucketing across sessions, devices, and processes.

## Applies If (ALL must hold)

- Experiment design is complete (hypothesis, primary metric, MDE, sample size) and runtime is needed.
- Multi-platform consistency: same user must get same variant on web, iOS, app, and email.
- Building an event pipeline joining exposure → conversion in a stats engine (Snowflake, ClickHouse).
- Wiring a feature flag into a real experiment with stratified randomization.

## Skip If (ANY kills it)

- Traffic too low to reach statistical power (under ~1k weekly users on the surface) — use qualitative methods.
- Changes affecting every user equally and irreversibly (DB schema migrations).
- Cosmetic tweaks where test cost exceeds shipping cost.
- Multi-armed scenarios with strong network effects (marketplace pricing) — A/B is biased; use switchback or geo splits.
- Compliance-bound flows (KYC, payments) where variant differences create audit problems.

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

- parent skill: `solo/dev/software-developer/`
