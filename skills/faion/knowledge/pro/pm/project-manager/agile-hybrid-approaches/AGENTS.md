---
slug: agile-hybrid-approaches
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Decision framework for selecting predictive / agile / named-hybrid delivery mode via Boehm + Turner 6-dimension score, with mid-project re-evaluation when metrics shift.
content_id: "4141eb7611ce134a"
complexity: deep
produces: decision-record
est_tokens: 4400
tags: [hybrid, waterfall, scrum, kanban, delivery-mode]
---
# Agile Hybrid Approaches

## Summary

**One-sentence:** Decision framework for selecting predictive / agile / named-hybrid delivery mode via Boehm + Turner 6-dimension score, with mid-project re-evaluation when metrics shift.

**One-paragraph:** Choosing between predictive (waterfall), agile (Scrum/Kanban), or named hybrid is a leading project-mode decision that's often made by inertia. This methodology codifies the Boehm + Turner home-ground model: score 6 dimensions (requirement volatility, team skill uniformity, failure cost, team size, culture fit, domain uncertainty) → recommend mode. Approach mismatch is detected via metrics (e.g., velocity volatility + escalation rate); re-evaluation is triggered mid-project. The output is a decision record with score + mode + named hybrid tilt + evaluation triggers.

**Ефективно для:**

- Programmes choosing delivery mode at inception.
- Programmes whose chosen mode is failing — mid-project re-evaluation.
- Multi-team programmes where different teams should run different modes.
- Regulated programmes that need predictive evidence + agile delivery.

## Applies If (ALL must hold)

- Programme has a delivery-mode decision to make or revisit.
- Teams can score the 6 dimensions with evidence.
- Mode change is feasible within the programme.
- Re-evaluation cadence (every quarter / phase gate) is observed.

## Skip If (ANY kills it)

- Mode is locked by contract — no decision available.
- Team has not run the candidate mode and cannot score culture fit.
- Programme < 4 weeks — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter + scope baseline | MD | scope-management |
| Team profile + skill matrix | table | HR |
| Domain uncertainty notes | MD | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Sponsor + delivery alignment underpins mode change. |
| `agile-ceremonies-setup` | Operationalises agile mode after decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — 6-dimension score required, evidence per dimension, named hybrid tilt, re-evaluation triggers, decision record committed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the mode-decision record | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: gather → score → recommend → debate → record → re-evaluate | 900 |
| `content/05-examples.xml` | optional | Worked decision record for a regulated programme | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping score state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-dimensions` | sonnet | Evidence-cited judgment per dimension. |
| `compute-recommendation` | haiku | Mechanical aggregation. |
| `named-hybrid-design` | opus | Cross-team synthesis of hybrid tilt + boundaries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/approach-decision.md` | Decision record skeleton with 6-dim score + hybrid tilt. |
| `templates/kanban-board.md` | Kanban column template for hybrid teams. |
| `templates/sprint-planning.md` | Hybrid sprint template (Scrum cadence + Kanban WIP). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agile-hybrid-approaches.py` | Schema-validate the decision record JSON. | Pre-commit + before mode change. |
| `scripts/approach-score.py` | Compute mode recommendation from 6-dim score. | On dimension change. |

## Related

- [[agile-ceremonies-setup]]
- [[scope-management]]
- [[stakeholder-engagement]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agile-hybrid-approaches input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
