---
slug: stakeholder-management
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Stakeholder register + power × interest × attitude grid + per-stakeholder engagement cadence + decision-rights map for PMs running cross-functional features and pre-launch GTM.
content_id: "a252fc7e580f13f1"
complexity: medium
produces: spec
est_tokens: 5500
tags: [stakeholder-management, cross-functional, communication, decision-rights, governance]
---
# Stakeholder Management

## Summary

**One-sentence:** Stakeholder register + power × interest × attitude grid + per-stakeholder engagement cadence + decision-rights map for PMs running cross-functional features and pre-launch GTM.

**One-paragraph:** Three-axis register (power/interest/attitude), per-quadrant engagement cadence, written decision-rights (D/I/V), pre-registered escalation triggers, mandatory upward-comms cadence. Output: stakeholder-register markdown + comms-plan YAML.

**Ефективно для:**

- PM inherits product line — потрібна мапа 'з ким говорити' до першого 1:1.
- Exec flags 'surprised' — fix є explicit upward-comms cadence.
- Feature crosses 3+ functional silos — register codifies brokerage rules.
- Pre-launch GTM coordination: marketing/sales/support/legal sign Ready gate.

## Applies If (ALL must hold)

- PM inherits a product line and needs to know who to talk to before the first 1:1.
- An executive flags being 'surprised' — fix is explicit upward-comms cadence.
- A feature crosses 3+ functional silos.
- Two stakeholders disagree publicly — use power × interest × attitude to choose the right forum.
- Pre-launch GTM coordination: marketing, sales, support, legal must each sign a Ready gate.

## Skip If (ANY kills it)

- Single-team product with no cross-functional surface.
- Pre-PMF with no exec sponsors.
- Agency project where stakeholder is one client contact (use simpler RACI).
- Existing register <=90 days old without org change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | diagram | HR |
| Project scope | doc | PM |
| Decision history | log | previous PM |
| Comms cadence baseline | doc | Head of Product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Self-reference: nested escalation logic depends on the register. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: register with 3 axes, per-quadrant cadence, decision-rights map, escalation criteria, mandatory upward comms | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for stakeholder-register + comms-plan | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: two-axis grid, ad-hoc cadence, decision re-litigation, exec surprise | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: list stakeholders -> tag axes -> map cadence -> assign decision rights -> pre-register escalation | 800 |
| `content/05-examples.xml` | medium | Worked register + comms plan for pre-launch GTM | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on cross-functional surface + register age | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `register-author` | sonnet | Build the register from org chart + project scope. |
| `cadence-derive` | haiku | Map quadrant to cadence template. |
| `escalation-trigger-fire` | sonnet | Decide whether the situation matches pre-registered triggers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Register skeleton with 3 axes + cadence + decision rights. |
| `templates/communication-plan.md` | Per-stakeholder comms plan template. |
| `templates/pm-attention-diff.py` | Compute PM attention split per stakeholder vs target. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-management.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[release-planning]]
- [[product-explainability]]
- [[okr-cascade-multi-squad]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
