---
slug: post-handover-warranty-runbook
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pinned runbook for outsource delivery teams during the 30/60/90-day warranty window — numbered steps with precondition, actor, artefact, rollback, and run-record per execution.
content_id: "23caa4852200a63e"
complexity: medium
produces: playbook-step
est_tokens: 3800
tags: [runbook, warranty, handover, outsource, sla]
---
# Post-Handover Warranty Runbook

## Summary

**One-sentence:** Pinned runbook for outsource delivery teams during the 30/60/90-day warranty window — numbered steps with precondition, actor, artefact, rollback, and run-record per execution.

**One-paragraph:** Post-handover warranty windows have a recurring on-call shape that neither pure project delivery nor pure operations covers. This methodology pins the artefact: a fixed-shape runbook with named owner, evidence anchors, wall-clock budget per phase, and a published review cadence. Steps carry preconditions, named actors (role+system), produced artefacts, and explicit rollback or STOP branches. After each execution, a structured run-record is committed to the postmortem feeder folder. The runbook is reviewed against outcomes at the next iteration.

**Ефективно для:**

- Outsource delivery contracts with 30/60/90-day warranty windows.
- Handovers to client in-house teams with named runbook owner.
- Regulated handovers needing audit-trail of execution.
- Teams running ≥3 instances per year (review cadence pays off).

## Applies If (ALL must hold)

- Handover to client in-house team has a published cadence.
- Outsource delivery specialist owns the artefact.
- Team uses version-controlled or wiki-style space for the runbook.
- Trigger event is observable (alert, ticket, calendar, threshold).

## Skip If (ANY kills it)

- One-shot work with no recurrence — single doc, not versioned runbook.
- Team has < 3 instances per year.
- Regulator mandates a different shape (use the template).
- No named owner available — defer until ownership resolves.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Handover spec | MD / signed PDF | delivery contract |
| SLA window definition | MD | contract |
| On-call rota | PagerDuty / ICS | operations |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `project-closure-with-lessons-extraction` | Provides closure artefacts that seed the runbook. |
| `communications-management` | Channels for escalation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — preconditions, named actor, rollback or STOP, timeboxed phases, post-action record | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the runbook artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with detector + repair | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold → populate → walk-test → publish → review | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping runbook state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-runbook` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Select correct evidence per step. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis of behaviour change. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with not_applicable markers. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-post-handover-warranty-runbook.py` | Schema-validate runbook JSON. | Pre-merge. |
| `scripts/staleness-check.py` | Flag runbooks past their review window. | Weekly cron. |

## Related

- [[project-closure-with-lessons-extraction]]
- [[communications-management]]
- [[stakeholder-engagement]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the post-handover-warranty-runbook input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
