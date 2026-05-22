---
slug: ba-planning
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A six-step framework that defines how BA work will be performed before requirements gathering begins: selecting plan-driven, change-driven, or hybrid approach based on context; building the stakeholder list; scheduling elicitation activities; specifying deliverables; and establishing governance (approver, change process, escalation path).
content_id: "4442ac0007c37656"
tags: [ba-planning, stakeholder-analysis, approach-selection, governance, requirements-elicitation]
---
# Business Analysis Planning

## Summary

**One-sentence:** A six-step framework that defines how BA work will be performed before requirements gathering begins: selecting plan-driven, change-driven, or hybrid approach based on context; building the stakeholder list; scheduling elicitation activities; specifying deliverables; and establishing governance (approver, change process, escalation path).

**One-paragraph:** A six-step framework that defines how BA work will be performed before requirements gathering begins: selecting plan-driven, change-driven, or hybrid approach based on context; building the stakeholder list; scheduling elicitation activities; specifying deliverables; and establishing governance (approver, change process, escalation path). The BA Approach Document is stored as a versioned Markdown+YAML file in git, refreshed on a 14-day cadence.

## Applies If (ALL must hold)

- Kicking off a multi-stakeholder initiative (>3 stakeholder groups) where elicitation, deliverables, and approval flow must be agreed before requirements work starts.
- Regulated programs (medical, fintech, gov, ISO 9001/SOX) where auditors expect a documented BA approach with named approvers.
- Hybrid plan-driven + change-driven engagements where artifacts must be explicitly declared as baselined vs. living.
- Spinning up a new BA capability inside a delivery team that had none previously.
- Seeding inputs for stakeholder-analysis, elicitation-techniques, and requirements-lifecycle.

## Skip If (ANY kills it)

- Solo founder building an MVP — planning ceremony is overhead; use a one-page lean canvas.
- Pure XP/Scrum teams running on a refined backlog with a Definition of Ready that already encodes the BA approach.
- Initiatives shorter than ~2 weeks of effort with one stakeholder — the plan costs more than the work it organizes.
- When the sponsor refuses to commit a governance model in writing — without an approver the plan is shelfware.
- Throwaway prototypes, spikes, or research probes.

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

- parent skill: `pro/ba/business-analyst/`
