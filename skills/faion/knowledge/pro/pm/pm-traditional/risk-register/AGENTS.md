---
slug: risk-register
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Living, version-controlled register of identified threats and opportunities, each row carrying owner, trigger, P×I score, strategy, and weekly-reviewed status.
content_id: "b0aa5c60bb749e72"
complexity: medium
produces: spec
est_tokens: 4200
tags: [risk-register, pmbok, register, tracking, accountability]
---
# Risk Register

## Summary

**One-sentence:** Living, version-controlled register of identified threats and opportunities, each row carrying owner, trigger, P×I score, strategy, and weekly-reviewed status.

**One-paragraph:** The register is the artefact produced by `risk-management`: a tabular log where every row commits to a named owner, observable trigger, P (VL-VH), I (VL-VH), risk score (P×I), strategy, source evidence, status, and last-reviewed date. It is reviewed weekly and risks are closed explicitly with outcome labels. The register is the audit-trail control mechanism; without it, risks become folklore. Output is a versioned register file (CSV/Markdown/Jira) reviewed against outcomes weekly.

**Ефективно для:**

- Multi-month delivery needing a single source of truth for risks across teams.
- Audited or regulated programmes requiring register with IDs, owners, decision history.
- Programmes with defended quantitative contingency reserves.
- Cross-vendor work where risks span ownership boundaries.

## Applies If (ALL must hold)

- Multi-month delivery needing single source of truth for risks.
- Audited/regulated programme requires owners + decision history.
- Cross-vendor work where risks span ownership boundaries.
- Contingency reserves must be defended quantitatively.

## Skip If (ANY kills it)

- Solo or hobby project — RISKS.md is enough.
- Pure-Scrum team running impediment + retro coverage already.
- Spike or discovery work where most 'risks' are research questions.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| risk-management output | list of scored risks | risk-management |
| Cost baseline | spreadsheet | cost-estimation |
| Prior register snapshot | CSV / MD | version control |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `risk-management` | Produces the risks that populate the register. |
| `stakeholder-register` | Source of named accountable owners. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — id format, mandatory columns, evidence, status set, audit retention | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for register artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold → populate → review → reconcile → publish | 800 |
| `content/05-examples.xml` | optional | Worked register snippet for a 4-month delivery | 500 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping register state → rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-register` | haiku | Template fill; no judgment. |
| `diff-vs-prior` | haiku | Mechanical diff NEW/CHANGED/CLOSED/STALE. |
| `audit-coverage` | sonnet | Cross-reference register against charter + WBS coverage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Living register table. |
| `templates/risk-card.md` | Detailed single-risk record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-risk-register.py` | Schema-validate the register JSON artefact. | Pre-commit + before steering review. |
| `scripts/risk-audit.py` | Static-analyse the register: stale rows, missing owners, missing triggers. | Weekly cron. |

## Related

- [[risk-management]]
- [[schedule-development]]
- [[cost-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the risk-register input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
