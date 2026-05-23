---
slug: stakeholder-engagement
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Identify stakeholders, map on Power/Interest grid, default cadence per quadrant, store register as version-controlled YAML, refresh quarterly minimum; triangulate attitude with behavioural signal.
content_id: "4e58334885338462"
complexity: medium
produces: spec
est_tokens: 4700
tags: [stakeholder-management, power-interest-grid, engagement-strategy, communication-plan, register]
---
# Stakeholder Engagement

## Summary

**One-sentence:** Identify stakeholders, map on Power/Interest grid, default cadence per quadrant, store register as version-controlled YAML, refresh quarterly minimum; triangulate attitude with behavioural signal.

**One-paragraph:** Five-step process: identify all stakeholders, analyze Power/Interest (with Mitchell-Agle-Wood salience overlay for political risk), assign engagement strategy per quadrant, execute communication plan with default cadence (Manage Closely=weekly 1:1, Keep Satisfied=biweekly, Keep Informed=monthly, Monitor=release-only), and monitor/adapt with quarterly refresh minimum. Store register as YAML in git so changes produce a diff history. Triangulate attitude with at least one behavioural signal — self-report is unreliable.

**Ефективно для:**

- Project kickoff for cross-functional initiative with >5 named parties
- Programmes with political risk (M&A, reorg, vendor consolidation, regulated rollout)
- Multi-stakeholder transformation programmes (cloud migration, ERP)
- Public-facing programmes with citizen/community stakeholders

## Applies If (ALL must hold)

- Project kickoff for any cross-functional initiative with more than 5 named parties
- Programs with significant political risk: M&A integration, reorgs, vendor consolidation
- Multi-stakeholder transformation programs (cloud migration, ERP)
- Public-facing programs (government, NGO, infrastructure) with citizen / community stakeholders
- Pre-RFP or vendor-selection efforts where the buying committee has hidden influencers

## Skip If (ANY kills it)

- Solo founders or very small teams (under 5 stakeholders)
- One-off internal hotfixes or refactors with no business stakeholder change
- Anonymous open-source community projects
- Crisis or incident response — incident command structure replaces engagement plan during P0

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | CSV / Graph export | Microsoft Entra ID / Workday |
| Charter | Markdown | sponsor + PM |
| Kickoff transcript | text | kickoff facilitator |
| Hidden-stakeholder checklist | list | legal / infosec / procurement / works-council / accessibility |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-register]] | Register schema and storage convention |
| [[scope-management]] | Requirements anchor source stakeholders |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: default-cadence-by-quadrant, evidence-required-for-attitude, triangulate-with-behaviour, hidden-stakeholder-pass, register-in-git | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-register` | sonnet | Seeded from org chart + charter; never invent names |
| `triangulate-attitude` | sonnet | Cross-reference self-report with behavioural signals |
| `compute-cadence` | haiku | Quadrant → default cadence mapping |

## Templates

| File | Purpose |
|------|---------|
| `templates/register.yaml` | Stakeholder register schema: id, power, interest, attitude, quadrant, cadence, last_engaged |
| `templates/engagement-plan.md` | Engagement plan with quadrant strategies and per-stakeholder cadence |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/engagement-due.py` | Flag stakeholders past their engagement cadence deadline | Weekly cron |
| `scripts/validate-stakeholder-engagement.py` | Lint register schema + evidence-required-for-attitude rule | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[stakeholder-register]]
- [[scope-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
