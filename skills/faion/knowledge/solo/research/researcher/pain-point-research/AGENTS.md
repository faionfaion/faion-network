---
slug: pain-point-research
tier: solo
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A systematic methodology for discovering and scoring customer pain points across public sources (Reddit, G2, App Store, Quora, Upwork).
content_id: "5753a01fe410ea11"
tags: [research, pain-points, customer-research, problem-validation, scoring-framework]
---
# Pain Point Research

## Summary

**One-sentence:** A systematic methodology for discovering and scoring customer pain points across public sources (Reddit, G2, App Store, Quora, Upwork).

**One-paragraph:** A systematic methodology for discovering and scoring customer pain points across public sources (Reddit, G2, App Store, Quora, Upwork). The rule: define audience + context first, mine at least 3 source tiers, capture verbatim quotes with URLs, score each pain on 5 weighted factors (Frequency 30%, Severity 25%, Reach 20%, Spend 15%, Alternatives 10%), then extract root causes via 5-Whys for the top findings.

## Applies If (ALL must hold)

- Pre-MVP: target audience defined but no validated problem yet.
- Choosing between 3-5 candidate ideas — score the underlying pains to break ties.
- Exploring an unfamiliar niche where domain intuition is weak.
- Repurposing existing research (G2 reviews, Reddit threads) into a structured opportunity backlog.

## Skip If (ANY kills it)

- You already have paying users — switch to user interviews and cancellation post-mortems; stranger pain points add noise.
- Highly regulated domains (healthcare, finance) where complaints are NDA'd and public signal is misleading.
- B2B enterprise where buyers don't post complaints publicly — use expert calls and analyst reports instead.
- Quantitative effect sizes are required — this methodology yields qualitative signal only.

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
