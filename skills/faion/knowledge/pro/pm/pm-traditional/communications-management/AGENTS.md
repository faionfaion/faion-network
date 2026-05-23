---
slug: communications-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Plan, execute, and monitor stakeholder communications so the right people receive the right information at the right time via comms plan + status reports + action extraction.
content_id: "85d5fba2ceef8dea"
complexity: medium
produces: config
est_tokens: 4200
tags: [communications, stakeholders, status-reporting, meetings, comms-plan]
---
# Communications Management

## Summary

**One-sentence:** Plan, execute, and monitor stakeholder communications so the right people receive the right information at the right time via comms plan + status reports + action extraction.

**One-paragraph:** Plan, execute, and monitor stakeholder communications so the right people receive the right information at the right time via comms plan + status reports + action extraction. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-communications-management.py` enforces the output contract.

**Ефективно для:**

- Multi-stakeholder programs with varied information needs (exec, ops, dev, vendor).
- Distributed teams with timezone-driven async-first comms.
- Crisis comms during incidents or scope escalations.
- Programs where status fatigue erodes stakeholder engagement.

## Applies If (ALL must hold)

- Stakeholder register exists with ≥3 segments.
- Comms plan can be authored before delivery starts.
- Tooling exists for status distribution (email, Slack, dashboard).

## Skip If (ANY kills it)

- Single-stakeholder side project.
- Team < 3 with co-located workspace and verbal sync.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder register | CSV/YAML | PM |
| Comms channels inventory | list | PM + IT |
| Status report cadence | weekly/biweekly | Sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[seven-performance-domains]] | comms lives within Stakeholders domain |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-comms-plan` | sonnet | Judgement: channel + cadence per segment. |
| `extract-actions` | haiku | Mechanical: regex/heuristic on transcript. |
| `score-engagement` | haiku | Roll-up of opens/replies/attendance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comms-plan.md` | Comms plan template: segment × channel × cadence × content × owner |
| `templates/action-extractor.py` | Action extraction from meeting transcript → owner + due + linked issue |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-communications-management.py` | Validate the config artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[seven-performance-domains]]
- [[change-control]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

