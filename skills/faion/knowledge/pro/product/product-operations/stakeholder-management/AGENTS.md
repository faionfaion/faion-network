---
slug: stakeholder-management
tier: pro
group: product
domain: product-operations
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Stakeholder management identifies everyone affected by a product (end users, decision makers, influencers, builders, support, external), maps them on a Power/Interest grid with an explicit attitude column (Supporter/Neutral/Resistor), assigns a named owner and engagement cadence per stakeholder, and codifies approval gates so agents can block SDD transitions until named approvers sign off.
content_id: "248ec3b180dc48b0"
tags: [stakeholder, engagement, management, communication, relationships]
---
# Stakeholder Management

## Summary

**One-sentence:** Stakeholder management identifies everyone affected by a product (end users, decision makers, influencers, builders, support, external), maps them on a Power/Interest grid with an explicit attitude column (Supporter/Neutral/Resistor), assigns a named owner and engagement cadence per stakeholder, and codifies approval gates so agents can block SDD transitions until named approvers sign off.

**One-paragraph:** Stakeholder management identifies everyone affected by a product (end users, decision makers, influencers, builders, support, external), maps them on a Power/Interest grid with an explicit attitude column (Supporter/Neutral/Resistor), assigns a named owner and engagement cadence per stakeholder, and codifies approval gates so agents can block SDD transitions until named approvers sign off.

## Applies If (ALL must hold)

- Cross-functional product launch with 5+ named stakeholders where misalignment has already cost time once.
- Re-org or PM handover: dump every stakeholder relationship into a register so the incoming PM can start without rediscovery.
- Roadmap quarter start: refresh the grid, decide which stakeholders move from Inform to Partner for upcoming bets.
- An SDD feature has a named approval gate (legal, security, head of sales) — codify it so the executor agent blocks until the approver signs off.
- Building a multi-agent comms pipeline where status-bot, release-notes-bot, and executive-summary-bot all pull audience from a shared register.

## Skip If (ANY kills it)

- Solo founder pre-revenue with only customers and family — a 5-line note in the project README is sufficient.
- Internal dev-tools used by under 10 engineers in the same Slack channel — async stand-up + RFC comments cover it.
- Crisis/incident mode: run incident-management first, restore service, update the register post-mortem.
- When the problem is "we don't know who's doing what work" — use raci-matrix or WBS, not this.

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

- parent skill: `pro/product/product-operations/`
