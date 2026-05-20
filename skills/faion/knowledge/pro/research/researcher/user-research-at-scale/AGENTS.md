---
slug: user-research-at-scale
tier: pro
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI-augmented research operations for N >= 500 sessions/week or >= 50 unmoderated tests, running a 9-stage pipeline: intake → sampling → instrumentation → collection → transcription → coding → synthesis → review → publish.
content_id: "6ff97c201f0b5419"
tags: [user-research, research-ops, qualitative-analysis, research-at-scale, ai-augmented-research]
---
# User Research at Scale

## Summary

**One-sentence:** AI-augmented research operations for N >= 500 sessions/week or >= 50 unmoderated tests, running a 9-stage pipeline: intake → sampling → instrumentation → collection → transcription → coding → synthesis → review → publish.

**One-paragraph:** AI-augmented research operations for N >= 500 sessions/week or >= 50 unmoderated tests, running a 9-stage pipeline: intake → sampling → instrumentation → collection → transcription → coding → synthesis → review → publish. Uses a frozen codebook with a separate proposed_codes overflow channel to prevent theme drift, and human-in-the-loop checkpoints before synthesis is published.

## Applies If (ALL must hold)

- N >= 500 sessions/week or >= 50 unmoderated tests where manual coding is the bottleneck.
- Continuous discovery teams needing a weekly pulse (Teresa Torres cadence).
- Product orgs with multiple teams running parallel studies (research-as-platform).
- Localization at scale — same study across 5+ languages, AI handles transcription + translation.
- Survey + behavior + interview triangulation when a single researcher cannot read everything.

## Skip If (ANY kills it)

- Small N (less than 10 deep interviews) — AI noise overwhelms signal; human coding is faster and richer.
- Strategic generative discovery where pattern-recognition beats throughput.
- Sensitive/regulated topics (health, finance, minors) requiring manual consent chains.
- Early-stage startups with less than 100 users — you do not have scale problems yet.
- Studies where rapport, body language, or longitudinal trust is the data.

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

- parent skill: `pro/research/researcher/`
