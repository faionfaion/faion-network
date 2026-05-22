---
slug: risk-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Risk management is a structured process for identifying, scoring, responding to, and monitoring project uncertainty — including both threats (negative risks) and opportunities (positive risks).
content_id: "1093aedd33356a45"
tags: [risk-management, pmbok, contingency, emv, uncertainty]
---
# Risk Management

## Summary

**One-sentence:** Risk management is a structured process for identifying, scoring, responding to, and monitoring project uncertainty — including both threats (negative risks) and opportunities (positive risks).

**One-paragraph:** Risk management is a structured process for identifying, scoring, responding to, and monitoring project uncertainty — including both threats (negative risks) and opportunities (positive risks). Every risk requires a trigger condition, an owner, and an explicit response strategy; risks without triggers are wishes, not plans.

## Applies If (ALL must hold)

- Multi-month delivery where surprises cost real money (more than $10k or two weeks)
- Regulated, safety-critical, or contractual work where an audit trail is required
- Cross-team programs with technical, vendor, and resource interdependencies
- Initiatives where a quantitative reserve (contingency) must be defended to finance
- Programs that exhibited risk failures on prior runs

## Skip If (ANY kills it)

- Pure exploratory R&D or spike work — fail-fast learning beats register hygiene
- Single-developer hobby project; an issue tracker risk label is enough
- Sub-two-week features where ceremony cost exceeds expected loss
- Pure-Scrum teams already running impediment and retro loops with adequate coverage

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
