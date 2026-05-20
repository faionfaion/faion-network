---
slug: surveys
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured data collection from many users through standardized questions that quantify attitudes, preferences, and experiences.
content_id: "55ff0d01c0e32d70"
tags: [surveys, questionnaires, quantitative-research, metrics, nps, sus]
---
# Surveys and Questionnaires

## Summary

**One-sentence:** Structured data collection from many users through standardized questions that quantify attitudes, preferences, and experiences.

**One-paragraph:** Structured data collection from many users through standardized questions that quantify attitudes, preferences, and experiences. Four survey types: satisfaction (CSAT, NPS), task-based (SUS, SEQ), preference (A vs B), and exploratory (usage patterns). Standard metrics require exact question wording and order — any deviation invalidates benchmarking against published norms.

## Applies If (ALL must hold)

- Validating qualitative findings at scale after interviews or diary studies.
- Tracking standardized UX metrics over time: NPS, CSAT, SUS, SEQ, CES — quarterly cohorts vs baseline.
- Post-task micro-surveys (1-2 questions) embedded in product after key flows.
- Segmenting a large user base: screener surveys to recruit participants for deeper qualitative work.
- Quantifying feature value across the full user base.

## Skip If (ANY kills it)

- "Why" questions — surveys give "what" and "how much"; interviews give "why".
- Sample below 100 — confidence intervals are too wide; do interviews instead.
- Highly emotional or sensitive topics — social desirability bias dominates self-report.
- Concept testing where artifact context matters — closed questions cannot substitute for showing the design.
- When results cannot drive action — running surveys you will ignore burns respondent trust permanently.

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

- parent skill: `pro/ux/ux-researcher/`
