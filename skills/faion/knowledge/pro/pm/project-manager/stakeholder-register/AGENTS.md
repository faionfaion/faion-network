---
slug: stakeholder-register
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identify every person or group who affects or is affected by the project, analyze their influence (power) and interest, classify into Power-Interest quadrants, and define an engagement strategy per quadrant.
content_id: "219540d3f32b17ad"
tags: [stakeholder-identification, power-interest-grid, register, yaml-schema, engagement-strategy]
---
# Stakeholder Register

## Summary

**One-sentence:** Identify every person or group who affects or is affected by the project, analyze their influence (power) and interest, classify into Power-Interest quadrants, and define an engagement strategy per quadrant.

**One-paragraph:** Identify every person or group who affects or is affected by the project, analyze their influence (power) and interest, classify into Power-Interest quadrants, and define an engagement strategy per quadrant. Store as YAML in source control; generate Markdown view from it. The rule: verify attitude through direct conversation, not inference — written communication is systematically polite and will produce false "Supportive" ratings.

## Applies If (ALL must hold)

- Project initiation: before charter sign-off, identify who funds, approves, uses, blocks
- Bid/proposal phase: capture buyer, economic buyer, technical buyer, end users
- Cross-functional rollout (pricing change, ToS update, new platform) with regulatory and legal stakeholders
- Agency engagements: register both client-side and agency-side stakeholders
- After a reorg or M&A where the old register is stale

## Skip If (ANY kills it)

- Fully internal personal-tool project with only you and your manager
- Pure agile team building for itself with one PO and no external dependencies
- Pre-discovery exploration where stakeholders are not yet defined — do problem framing first

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
