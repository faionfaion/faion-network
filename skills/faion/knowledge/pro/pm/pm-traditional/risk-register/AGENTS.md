---
slug: risk-register
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A living log of identified threats and opportunities, each with a probability (1–5), impact (1–5), risk score (P×I), chosen response strategy, named owner, trigger condition, and current status.
content_id: "370a99709358c1da"
tags: [risk-register, pmbok, register, tracking, accountability]
---
# Risk Register

## Summary

**One-sentence:** A living log of identified threats and opportunities, each with a probability (1–5), impact (1–5), risk score (P×I), chosen response strategy, named owner, trigger condition, and current status.

**One-paragraph:** A living log of identified threats and opportunities, each with a probability (1–5), impact (1–5), risk score (P×I), chosen response strategy, named owner, trigger condition, and current status. The register must be reviewed weekly and updated as risks materialize, pass, or merge.

## Applies If (ALL must hold)

- Multi-month delivery requiring a single source of truth for risks across teams
- Audited or regulated programs needing a register with IDs, owners, and decision history
- Programs with quantitative contingency reserves that must be defended to finance
- Cross-vendor or cross-org work where risks span ownership boundaries

## Skip If (ANY kills it)

- Solo or hobby projects — a RISKS.md checklist is enough
- Pure-Scrum teams running impediment and retro loops with adequate coverage
- Spike or discovery work where most "risks" are research questions

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
