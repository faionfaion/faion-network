---
slug: funnel-tactics-advanced
tier: pro
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization, and analytics event tracking patterns.
content_id: "d4891e73c2f8e2d6"
tags: [funnel, tactics, personalization, retargeting, advanced]
---
# Funnel Optimization Tactics — Advanced

## Summary

**One-sentence:** Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization, and analytics event tracking patterns.

**One-paragraph:** Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization, and analytics event tracking patterns. Advanced tactics recover abandoning users and direct test effort to highest-ICE hypotheses first. The rule: segment before personalizing — a single message to all users underperforms targeted messages by 15-40%.

## Applies If (ALL must hold)

- Baseline funnel is instrumented and you have step-level conversion data
- You want to recover abandoning users via exit intent or retargeting
- You need to prioritize a backlog of A/B test hypotheses using ICE scoring
- You are optimizing for a specific industry (SaaS, e-commerce, mobile app)

## Skip If (ANY kills it)

- No tracking in place — implement analytics events first
- Fewer than 1,000 monthly visitors — personalization overhead is not justified
- Still finding product-market fit — advanced tactics amplify a working funnel, not a broken one

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

- parent skill: `pro/marketing/conversion-optimizer/`
