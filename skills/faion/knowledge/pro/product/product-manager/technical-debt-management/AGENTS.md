---
slug: technical-debt-management
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A six-step framework for making technical debt visible, quantified, and systematically paid down — covering debt registration, impact scoring (interest × contagion / effort), capacity allocation, and prevention policies.
content_id: "b187463217f158b6"
tags: [technical-debt, product-management, engineering, prioritization, roadmap]
---
# Technical Debt Management

## Summary

**One-sentence:** A six-step framework for making technical debt visible, quantified, and systematically paid down — covering debt registration, impact scoring (interest × contagion / effort), capacity allocation, and prevention policies.

**One-paragraph:** A six-step framework for making technical debt visible, quantified, and systematically paid down — covering debt registration, impact scoring (interest × contagion / effort), capacity allocation, and prevention policies. Debt is classified into six types (deliberate, accidental, bit-rot, design, documentation, test) and prioritized against product work using the same backlog cadence.

## Applies If (ALL must hold)

- Roadmap velocity visibly declining despite stable headcount — need a quantified debt register to defend capacity allocation.
- Quarterly planning where 15-20% of capacity is reserved for paydown and engineering needs a prioritized list.
- Post-P0 outage or regression cluster where the post-mortem identifies debt as root cause.
- Before a major architectural change (auth rewrite, billing migration) — surface debt on the change surface so it is eliminated, not carried forward.
- Multi-repo solopreneur portfolio where debt silently compounds in lower-traffic repos.

## Skip If (ANY kills it)

- Pre-PMF prototypes where the entire codebase is deliberate prudent debt by design — track only debt that blocks the next validation experiment.
- Single-file scripts and one-shot data migrations — registration cost exceeds rewrite cost.
- When engineering has lost trust in PM prioritization — repair trust first via engineer-driven sprints, then introduce the scoring matrix.
- Bit-rot dependency upgrades that are fully automatable (Renovate / Dependabot) — automate, do not bureaucratize.
- Crisis quarters (runway < 6 months, regulator deadline) — freeze the register, ship survival features, resume after.

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

- parent skill: `pro/product/product-manager/`
