---
slug: ba-governance
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Establishes decision rights, change control, and communication planning for requirements work.
content_id: "f135322aa0bd55ca"
tags: [governance, ba, requirements, decision-rights, change-control]
---
# BA Governance

## Summary

**One-sentence:** Establishes decision rights, change control, and communication planning for requirements work.

**One-paragraph:** Establishes decision rights, change control, and communication planning for requirements work. Includes governance framework, communication planning, and elicitation preparation.

## Applies If (ALL must hold)

- Setting up decision rights, change control, and approval workflow for a new product or squad before requirements work starts.
- Projects crossing three or more stakeholder groups (sponsor, dev, ops, legal/compliance) that need a communication plan.
- Preparing elicitation logistics and technique selection before interviews or workshops begin.
- Auditing an existing requirements process where rework, scope drift, or sign-off ambiguity has been observed.
- Regulated builds (SOX, HIPAA, GDPR) where a decision audit trail is mandatory.

## Skip If (ANY kills it)

- Solo founder / single-team early MVP — formal governance burns time you do not have; use lightweight requirements-prioritization instead.
- Pure engineering refactors with no external stakeholders — governance overhead is waste; rely on PR review.
- Research spikes and discovery sprints where the goal is learning, not committing scope.
- Crisis incidents — use incident command, not governance workflow.

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

- parent skill: `pro/ba/ba-core/`
