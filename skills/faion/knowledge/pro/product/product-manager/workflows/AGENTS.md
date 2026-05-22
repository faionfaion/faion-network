---
slug: workflows
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Two core PM pipelines: Project Bootstrap (idea → constitution → TASK_000) and MLP Planning (MVP → Most Lovable Product).
content_id: "5855a9b1517a6537"
tags: [product-management, project-bootstrap, mlp-planning, roadmap, backlog]
---
# Product Manager Workflows

## Summary

**One-sentence:** Two core PM pipelines: Project Bootstrap (idea → constitution → TASK_000) and MLP Planning (MVP → Most Lovable Product).

**One-paragraph:** Two core PM pipelines: Project Bootstrap (idea → constitution → TASK_000) and MLP Planning (MVP → Most Lovable Product). Bootstrap is interactive and requires explicit user confirmation at Phase 4; MLP runs five `faion-mlp-agent` modes sequentially. Both pipelines treat `.aidocs/features/` as the planning source of truth and Jira/Linear as the execution mirror — never the reverse.

## Applies If (ALL must hold)

- New project bootstrap where `.aidocs/` is empty and `constitution.md` + `roadmap.md` need authoring before any code task.
- MVP-to-MLP transition after first usable build ships and produces real telemetry.
- Sprint kickoff and review ceremonies where backlog needs grooming, sizing, and tracker sync.
- Release coordination: changelog generation, release-notes draft, GTM handoff.
- Daily PM ritual: backlog re-prioritization, stakeholder digest, blocker surfacing.

## Skip If (ANY kills it)

- During SDD task execution itself — code tasks belong to `/faion` (sdd-batch-orchestrator workflow). PM workflow stops at TASK_000.
- One-off feature requests inside an active sprint — log to backlog via tracker API.
- Spec changes after spec freeze — route through change management.
- Solo Phase 1 before anything to prioritize — use `solo/product/product-planning/mvp-scoping` instead.

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

- parent skill: `pro/product/product-manager/`
