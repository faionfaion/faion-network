---
slug: change-control
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle.
content_id: "5a43867c425632e1"
tags: [change-control, change-management, scope, governance, approval]
---
# Change Control

## Summary

**One-sentence:** Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle.

**One-paragraph:** Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle. Tier authority by size: PM approves minor (less than 1 day, less than $500), Sponsor approves medium (1-5 days, less than $5k), CCB approves major. The rule: never auto-approve — the agent prepares the impact packet; a human approver signs off before implementation begins.

## Applies If (ALL must hold)

- Fixed-scope, fixed-budget engagements (agency contracts, SoWs) where every change has billing impact.
- Regulated environments (finance, healthcare, government) requiring an audit trail of decisions.
- Projects with multiple stakeholders submitting asks via different channels — register forces one queue.
- Late-stage projects (greater than 50% complete) where every change has compounded ripple effects.
- Programs where one project's change affects sibling projects.

## Skip If (ANY kills it)

- Pure agile teams with continuous backlog refinement — change is the default state, not the exception.
- Discovery/research phases — you want changes; controlling them defeats the purpose.
- Solo projects where you are both requester and approver — capture as a TODO, not a CR.

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

- parent skill: `pro/pm/project-manager/`
