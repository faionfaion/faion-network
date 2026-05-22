---
slug: trade-off-technical-debt
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Technical debt is the implied cost of rework caused by choosing an easier but limited solution now instead of a better approach that would take longer.
content_id: "7dd1f3a484b5823f"
tags: [technical-debt, trade-off, refactoring, architecture, speed-vs-quality]
---
# Technical Debt Trade-off Framework

## Summary

**One-sentence:** Technical debt is the implied cost of rework caused by choosing an easier but limited solution now instead of a better approach that would take longer.

**One-paragraph:** Technical debt is the implied cost of rework caused by choosing an easier but limited solution now instead of a better approach that would take longer. The Fowler quadrant classifies debt by deliberate/inadvertent and reckless/prudent axes. The key decision: is the deadline real and is the debt localized? Maintain a 15-20% debt budget; document every deliberate debt item with a trigger for repayment.

## Applies If (ALL must hold)

- Deciding whether to ship a feature with shortcuts or invest in clean implementation first.
- Deciding whether to refactor existing code before adding a new feature in the same area.
- Prioritizing which technical debt items to pay off in a given sprint or quarter.
- Classifying existing debt to communicate its severity and repayment urgency to stakeholders.

## Skip If (ANY kills it)

- When the "debt" is actually a fundamental design flaw — classify as an architectural risk requiring ATAM analysis, not a debt item.
- When the code area will not be touched again for 2+ years — low future impact means debt repayment ROI is negative; document and accept.

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
