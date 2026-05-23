---
slug: stakeholder-register
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Identify groups + individuals; rate Power on org-chart/budget-authority evidence; verify attitude via conversation; store as YAML in source control; refresh after each stage gate.
content_id: "7b8d538b00e040e4"
complexity: medium
produces: config
est_tokens: 4000
tags: [stakeholder-identification, power-interest-grid, register, yaml-schema, engagement-strategy]
---
# Stakeholder Register

## Summary

**One-sentence:** Identify groups + individuals; rate Power on org-chart/budget-authority evidence; verify attitude via conversation; store as YAML in source control; refresh after each stage gate.

**One-paragraph:** Identify every person or group who affects or is affected by the project, analyze influence (Power) and interest, classify into Power-Interest quadrants, define engagement strategy. Store as YAML in source control; generate Markdown view from it. Verify attitude through direct conversation — written communication is systematically polite and produces false 'Supportive' ratings. Keep PII (email, phone, salary) in a separate access-controlled file. Refresh after each stage gate; archive previous version to track attitude changes.

**Ефективно для:**

- Project initiation: before charter sign-off, identify who funds, approves, uses, blocks
- Bid / proposal phase: buyer, economic buyer, technical buyer, end users
- Cross-functional rollout (pricing change, ToS update, new platform)
- After reorg or M&A where old register is stale

## Applies If (ALL must hold)

- Project initiation: before charter sign-off, identify who funds, approves, uses, blocks
- Bid/proposal phase: capture buyer, economic buyer, technical buyer, end users
- Cross-functional rollout (pricing change, ToS update, new platform) with regulatory stakeholders
- Agency engagements: register both client-side and agency-side stakeholders
- After a reorg or M&A where the old register is stale

## Skip If (ANY kills it)

- Fully internal personal-tool project with only you and your manager
- Pure agile team building for itself with one PO and no external dependencies
- Pre-discovery exploration where stakeholders are not yet defined

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | CSV / Graph export | HR / Microsoft Entra ID |
| Project charter draft | Markdown | sponsor / PM |
| Group authorities | list | explicit collective decision-makers (e.g. Security Council) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-engagement]] | Quadrant strategies |
| [[raci-matrix]] | Role attribution flows into RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: groups-as-groups, evidence-not-gut-feel, verify-attitude-in-conversation, attitude-unknown-without-evidence, pii-separated | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-register` | sonnet | Seeded from org chart + charter; never invent names |
| `classify-quadrant` | haiku | Influence × interest mapping |
| `flag-pii-leak` | sonnet | Scrub before commit |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-profile.md` | Individual stakeholder profile with interests, concerns, and engagement history |
| `templates/register.yaml` | Register schema: id, role, dept, influence, impact, attitude, quadrant, comms.cadence, last_touch |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-register.py` | Lint register schema + group-not-split-to-individuals + evidence-for-attitude | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[stakeholder-engagement]]
- [[raci-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
