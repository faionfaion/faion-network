---
slug: risk-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identify threats and opportunities, rate them by probability and impact, assign owners with observable triggers, plan responses, and monitor weekly.
content_id: "1093aedd33356a45"
tags: [risk-management, probability, impact, emv, contingency]
---
# Risk Management

## Summary

**One-sentence:** Identify threats and opportunities, rate them by probability and impact, assign owners with observable triggers, plan responses, and monitor weekly.

**One-paragraph:** Identify threats and opportunities, rate them by probability and impact, assign owners with observable triggers, plan responses, and monitor weekly. The rule: every risk must have a named owner (a person, not "the team") and explicit triggers — observable signals that convert an abstract risk into an actionable event. "Accept" is not a free pass; it requires a contingency budget line equal to the risk's EMV.

## Applies If (ALL must hold)

- Project initiation: build initial risk register before charter sign-off
- Stage-gate reviews: refresh probability/impact and trigger statuses
- Pre-launch (T-2 weeks): focused launch-risk pass with rollback plans
- After incidents: feed lessons back as new risks for similar projects
- High-uncertainty domains: new technology, new vendor, regulatory change

## Skip If (ANY kills it)

- Trivial internal task (1 person, under 1 week, no external dependency) — overhead exceeds value
- Pure agile teams with strong incremental delivery — short cycles already de-risk; use a "top 5" sticky list
- Crisis already in progress — switch to incident response; add lessons to register afterward

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

- parent skill: `pro/pm/project-manager/`
