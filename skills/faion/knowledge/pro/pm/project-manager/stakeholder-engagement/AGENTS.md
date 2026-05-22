---
slug: stakeholder-engagement
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured process to identify all parties affected by or affecting a project, map each on the Power/Interest grid, assign an engagement strategy per quadrant, and execute a communication cadence — stored as version-controlled YAML register so changes produce a diff history and evidence-backed attitudes.
content_id: "87ae9864d47f451a"
tags: [stakeholder-management, power-interest-grid, engagement-strategy, communication-plan, register]
---
# Stakeholder Engagement

## Summary

**One-sentence:** A structured process to identify all parties affected by or affecting a project, map each on the Power/Interest grid, assign an engagement strategy per quadrant, and execute a communication cadence — stored as version-controlled YAML register so changes produce a diff history and evidence-backed attitudes.

**One-paragraph:** A structured process to identify all parties affected by or affecting a project, map each on the Power/Interest grid, assign an engagement strategy per quadrant, and execute a communication cadence — stored as version-controlled YAML register so changes produce a diff history and evidence-backed attitudes. Engagement is continuous; register must refresh quarterly minimum.

## Applies If (ALL must hold)

- Project kickoff for any cross-functional initiative with more than 5 named parties
- Programs with significant political risk: M&A integration, reorgs, vendor consolidation, regulated rollouts
- Multi-stakeholder transformation programs (cloud migration, ERP) with sponsors, champions, blockers, and external auditors
- Public-facing programs (government, NGO, infrastructure) with citizen/community stakeholders
- Pre-RFP or vendor-selection efforts where the buying committee has hidden influencers

## Skip If (ANY kills it)

- Solo founders or very small teams (under 5 stakeholders) — direct conversation beats matrix overhead
- One-off internal hotfixes or refactors with no business stakeholder change — RACI alone is enough
- Anonymous open-source community projects — power/interest axes are meaningless without identity
- Crisis or incident response — incident command structure replaces engagement plan during P0
- When stakeholder identification is still unsolved — do BA stakeholder-analysis first to get a register

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
