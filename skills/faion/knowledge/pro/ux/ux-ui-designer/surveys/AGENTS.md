---
slug: surveys
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A research method for collecting structured data from large user populations through standardized questions — covering satisfaction (NPS, CSAT, SUS), task ease (SEQ), and feature preference — to quantify user attitudes and validate qualitative findings at scale.
content_id: "55ff0d01c0e32d70"
tags: [research, surveys, quantitative, user-research, metrics]
---
# Surveys and Questionnaires

## Summary

**One-sentence:** A research method for collecting structured data from large user populations through standardized questions — covering satisfaction (NPS, CSAT, SUS), task ease (SEQ), and feature preference — to quantify user attitudes and validate qualitative findings at scale.

**One-paragraph:** A research method for collecting structured data from large user populations through standardized questions — covering satisfaction (NPS, CSAT, SUS), task ease (SEQ), and feature preference — to quantify user attitudes and validate qualitative findings at scale.

## Applies If (ALL must hold)

- Quantitative validation of qualitative findings at N≥100.
- Tracking standard UX metrics over time: NPS, SUS, CSAT, SEQ.
- Segmenting users (new vs. power, free vs. paid) to measure satisfaction or feature value.
- Pre/post launch comparison of perceived ease, trust, or feature impact.

## Skip If (ANY kills it)

- You do not yet know which questions to ask — run interviews first; an ill-formed survey produces noise.
- Sample <30 — descriptive statistics are unreliable; use qualitative methods instead.
- You need behavioral data (clicks, time on task) — analytics or usability tests, not self-report.
- High-stakes decisions where social-desirability bias dominates (e.g., willingness-to-pay overestimated 2-4x by surveys).

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

- parent skill: `pro/ux/ux-ui-designer/`
