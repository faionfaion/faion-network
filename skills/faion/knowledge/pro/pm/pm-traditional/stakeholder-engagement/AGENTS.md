---
slug: stakeholder-engagement
tier: pro
group: pm
domain: pm-traditional
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Systematic identification, classification, and engagement of everyone who affects or is affected by the project.
content_id: "87ae9864d47f451a"
tags: [stakeholders, engagement, power-interest, communication, relationship-management]
---
# Stakeholder Engagement

## Summary

**One-sentence:** Systematic identification, classification, and engagement of everyone who affects or is affected by the project.

**One-paragraph:** Systematic identification, classification, and engagement of everyone who affects or is affected by the project. The core artifact is a YAML-based stakeholder register (power, interest, attitude with evidence, quadrant, cadence, owner) stored in git so that engagement history is a diff log. Attitude assertions without evidence default to "unknown" — optimistic defaults ("supportive") are a known agent failure mode and a trust risk.

## Applies If (ALL must hold)

- Project kickoff for any cross-functional initiative with more than 5 named parties.
- Programs with high political risk: M&A, reorgs, regulated rollouts (HIPAA, SOX, GDPR).
- Pre-RFP / vendor selection where the buying committee has hidden influencers (security, procurement, FinOps).
- Multi-stakeholder transformation programs where power and interest shift across phases.
- Pair with communications-management so cadence in the register is reflected in the comms plan.

## Skip If (ANY kills it)

- Solo founders or teams under 5 stakeholders — direct conversation beats matrix overhead.
- One-off internal hotfixes with no business stakeholder change — RACI is sufficient.
- Crisis/incident response — incident command structure replaces engagement plan during a P0.
- When stakeholder identification is unsolved — run BA stakeholder-analysis first to populate the register.

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

- parent skill: `pro/pm/pm-traditional/`
