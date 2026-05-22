---
slug: strategy-analysis-gap-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Gap analysis identifies what must change by joining current-state measurements with future-state targets for each area.
content_id: "a8eb0e9cda87e1d4"
tags: [strategy-analysis, gap-analysis, babok, prioritization, measurement]
---
# Strategy Analysis: Gap Analysis

## Summary

**One-sentence:** Gap analysis identifies what must change by joining current-state measurements with future-state targets for each area.

**One-paragraph:** Gap analysis identifies what must change by joining current-state measurements with future-state targets for each area. Every gap row carries: area, current metric value, future metric target, gap size, gap unit, priority (H/M/L), and an evidence URL. Gaps without numeric deltas cannot be prioritized and must be returned for re-measurement. A dependency DAG identifies which gaps block others so prioritization is not popularity-weighted.

## Applies If (ALL must hold)

- After current-state assessment is signed off AND future state is locked by the exec sponsor — both inputs are required; running gap analysis on unsigned inputs produces gaps that shift when the inputs shift.
- Any initiative requiring a change strategy: the gap analysis is the prioritized input to option evaluation.
- Portfolio planning: gap analysis across N initiatives establishes a shared prioritization surface — which gaps are shared, which are blocking, which are independent.
- Regulatory-driven change: the gap between the regulator's future-state requirements and the org's current state is the compliance gap; each row carries the regulatory citation as evidence_url.

## Skip If (ANY kills it)

- Before future state is locked — gaps computed against a draft future state will change when the future state is finalized; the work is wasted.
- Before current-state assessment is complete — gaps without a measured current-state baseline are guesses, not analysis.
- Single-area tactical changes with an obvious and agreed gap — overhead exceeds value; a two-line ADR is sufficient.

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

- parent skill: `pro/ba/business-analyst/`
