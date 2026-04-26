# Product Manager Workflows

## Summary

Two core PM pipelines: Project Bootstrap (idea → constitution → TASK_000) and MLP Planning (MVP → Most Lovable Product). Bootstrap is interactive and requires explicit user confirmation at Phase 4; MLP runs five `faion-mlp-agent` modes sequentially. Both pipelines treat `.aidocs/features/` as the planning source of truth and Jira/Linear as the execution mirror — never the reverse.

## Why

Without a structured bootstrap pipeline, projects start without a constitution, backlog items lack FR/AC numbering, and RICE scores are never assigned. The MLP transition is where "minimum viable" products become products people love — but only when grounded in real competitor evidence and telemetry, not speculation. These workflows enforce the required sequencing and artifacts.

## When To Use

- New project bootstrap where `.aidocs/` is empty and `constitution.md` + `roadmap.md` need authoring before any code task.
- MVP-to-MLP transition after first usable build ships and produces real telemetry.
- Sprint kickoff and review ceremonies where backlog needs grooming, sizing, and tracker sync.
- Release coordination: changelog generation, release-notes draft, GTM handoff.
- Daily PM ritual: backlog re-prioritization, stakeholder digest, blocker surfacing.

## When NOT To Use

- During SDD task execution itself — code tasks belong to `faion-feature-executor`. PM workflow stops at TASK_000.
- One-off feature requests inside an active sprint — log to backlog via tracker API.
- Spec changes after spec freeze — route through change management.
- Solo Phase 1 before anything to prioritize — use `solo/product/product-planning/mvp-scoping` instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-bootstrap-pipeline.xml` | 7-phase bootstrap flow, output structure, Phase 4 confirmation rule |
| `content/02-mlp-planning.xml` | MLP 5-mode sequential flow, WOW feature constraints, cap at 7 items |
| `content/03-numbering-conventions.xml` | Feature/task/requirement/AC numbering patterns and lock rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/rice-reorder.sh` | Rank backlog by RICE score, write sorted INDEX.md |
