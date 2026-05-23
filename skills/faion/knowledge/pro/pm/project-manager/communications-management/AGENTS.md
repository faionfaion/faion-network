---
slug: communications-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Structured who-what-when-how matrix (Communications Plan + RACI + decision log + meeting cadence) so each stakeholder gets the right artefact at the right tempo.
content_id: "2dfe89c0a1b3c4d5"
complexity: medium
produces: spec
est_tokens: 4200
tags: [communications, stakeholder, status-reporting, meetings, decision-log]
---
# Communications Management

## Summary

**One-sentence:** Structured who-what-when-how matrix (Communications Plan + RACI + decision log + meeting cadence) so each stakeholder gets the right artefact at the right tempo.

**One-paragraph:** Structured who-what-when-how matrix (Communications Plan + RACI + decision log + meeting cadence) so each stakeholder gets the right artefact at the right tempo.

**Ефективно для:**

- Проектів з ≥5 стейкхолдерів різного рівня поінформованості.
- Розподілених команд із cross-timezone-комунікацією.
- PMO, що централізує status reporting через комбінацію Slack/Email/Confluence.
- Програм із зовнішніми клієнтами, де комунікаційні SLA — частина контракту.

## Applies If (ALL must hold)

- Project has ≥5 distinct stakeholder groups.
- At least one external client / regulator requires status reports.
- Cross-timezone team (timezone gap ≥4h).
- Decisions need a written record for audit / handover.

## Skip If (ANY kills it)

- Two-person project — verbal coordination is enough.
- Single-stakeholder internal tooling project.
- Engagement < 1 week.
- Team uses an external comms framework (e.g. ITIL Service Comms) that supersedes this one.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[async-standup-template]] | Daily-cadence sub-pattern this plan absorbs. |
| [[lessons-learned]] | Decision log feeds retros. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `comms-matrix-author` | sonnet | Stakeholder × artefact × cadence synthesis. |
| `status-report-draft` | haiku | Fill the status template from metric inputs. |
| `decision-log-append` | haiku | Append immutable decision row. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comms-plan.md` | Comms-matrix: stakeholder, artefact, channel, owner, cadence, format. |
| `templates/status-report.md` | Weekly / biweekly status: progress, risks, decisions, next steps. |
| `templates/meeting-notes.md` | Notes template: attendees, decisions, action items with owners + due dates. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-communications-management.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[async-standup-template]]
- [[lessons-learned]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (stakeholder_count, external_client, timezone_gap, contract_sla) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
