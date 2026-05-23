---
slug: stakeholder-register
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Version-controlled catalogue of stakeholders with power, interest, attitude, evidence-grounded strategy, and 30-day staleness review.
content_id: "7b8d538b00e040e4"
complexity: medium
produces: spec
est_tokens: 4000
tags: [stakeholder-management, register, pmi, governance, attitude]
---
# Stakeholder Register

## Summary

**One-sentence:** Version-controlled catalogue of stakeholders with power, interest, attitude, evidence-grounded strategy, and 30-day staleness review.

**One-paragraph:** The stakeholder register is the static catalogue underpinning `stakeholder-engagement` and `stakeholder-engagement-advanced`. Each row carries id, role, power, interest, attitude (champion / supporter / neutral / critic / blocker), differentiated strategy, evidence source, and last_reviewed date. Rows older than 30 days are flagged stale and require re-validation against the org. Output: a YAML / JSON register committed alongside the project plan.

**Ефективно для:**

- Programmes with diverse stakeholder roles needing single source of truth.
- Regulated work requiring audit-trail of stakeholder identification.
- Multi-vendor work where stakeholder lists span ownership.
- Distressed projects needing re-identification of blockers.

## Applies If (ALL must hold)

- Programme has multiple distinct stakeholder roles (sponsor, steering, delivery).
- Audit-trail of stakeholder identification is needed for compliance.
- Cross-vendor stakeholders span ownership boundaries.
- Project will run for at least 30 days, justifying review cycle.

## Skip If (ANY kills it)

- Solo / single-team project with no external stakeholders.
- Pre-PMF startup where stakeholder map is the founder.
- Sub-2-week spike — register overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | diagram / list | HR / sponsor |
| Kickoff interview notes | MD | PM |
| Charter | signed PDF / MD | sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Register feeds the engagement cadence. |
| `communications-management` | Channels and templates for stakeholder communication. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — unique IDs, attitude enum, evidence per row, strategy length, 30-day staleness | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the register | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: list → classify → strategy → evidence → review | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping register state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-from-org-chart` | sonnet | Pattern-recognition over org chart + kickoff notes. |
| `audit-staleness` | haiku | Mechanical date arithmetic. |
| `attitude-assessment` | opus | Cross-signal synthesis of stakeholder behaviour. |

## Templates

| File | Purpose |
|------|---------|
| `templates/register-entry.yaml` | Single-row register entry template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-register.py` | Schema-validate the register JSON. | Pre-commit + monthly review. |
| `scripts/register_audit.py` | Audit register for missing evidence + stale rows. | Monthly cron. |

## Related

- [[stakeholder-engagement]]
- [[stakeholder-engagement-advanced]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the stakeholder-register input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
