---
slug: trade-off-decision-matrix
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build a weighted decision matrix to compare 3-5 architecture options across scored criteria.
content_id: "53ab2d8e7637cb61"
tags: [decision-matrix, trade-off, architecture, scoring, criteria]
---
# Trade-off Decision Matrix

## Summary

**One-sentence:** Build a weighted decision matrix to compare 3-5 architecture options across scored criteria.

**One-paragraph:** Build a weighted decision matrix to compare 3-5 architecture options across scored criteria. Run sensitivity analysis to verify the winner is stable. The standard 2-4h checklist covers context, option discovery, criteria definition, option evaluation, trade-off identification, risk analysis, and documentation.

## Applies If (ALL must hold)

- Technology selection or vendor comparison with 3-5 viable options.
- Any decision where criteria weights are contested among stakeholders.
- Standard 2-4h trade-off analysis for significant technical decisions with moderate impact.
- When you need to document the objective basis for a recommendation to stakeholders.

## Skip If (ANY kills it)

- Type-1 irreversible decisions with major business impact — use ATAM for deeper analysis instead of just a matrix.
- Type-2 reversible decisions where the wrong choice costs less than the analysis — decide fast and iterate.
- When criteria cannot be agreed on first — resolve stakeholder alignment before scoring.

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

- parent skill: `solo/dev/software-architect/`
