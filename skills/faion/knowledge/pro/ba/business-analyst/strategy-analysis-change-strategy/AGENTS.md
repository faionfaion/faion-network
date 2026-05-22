---
slug: strategy-analysis-change-strategy
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The change strategy determines how to close the prioritized gaps from the gap analysis.
content_id: "3aec35580499c2ce"
tags: [strategy-analysis, change-strategy, babok, options-evaluation, decision-making]
---
# Strategy Analysis: Change Strategy Formation

## Summary

**One-sentence:** The change strategy determines how to close the prioritized gaps from the gap analysis.

**One-paragraph:** The change strategy determines how to close the prioritized gaps from the gap analysis. It generates 3-5 options (build, buy, partner, modify, combination) plus a status-quo baseline, profiles each against cost / time / risk / capability criteria, and hands the option set to decision-analysis for weighted-matrix selection. The BA owns option generation and profiling; the decision-maker signs the recommendation before downstream SDD work begins.

## Applies If (ALL must hold)

- After gap analysis is complete and prioritized — change strategy formation requires a signed gap analysis as input.
- Any initiative where the business case will gate a significant spend — stakeholders need to see that alternatives were evaluated, not just the preferred option.
- Portfolio planning where multiple options across multiple initiatives compete for the same budget envelope — the evaluation matrix enables cross-initiative comparison.
- M&A integration planning: Day-1 / Day-100 / Day-365 plan options evaluated against the gap-priority map.
- Regulatory-driven change: the change strategy documents how compliance gaps will be closed and justifies the chosen path to auditors.

## Skip If (ANY kills it)

- Before gap analysis is signed — options cannot be evaluated without a prioritized gap list; the evaluation matrix has no rows to score against.
- When the decision-maker has already committed to a path publicly — document it as a directive; producing a multi-option analysis becomes theatre and damages BA credibility.
- Single-option technical fixes with an obvious solution and negligible blast radius — overhead exceeds value.

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
