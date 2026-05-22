---
slug: cog-walk-process
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The full structured process for running a cognitive walkthrough: defining prerequisites (persona, task, correct action sequence, interface), assembling 2-4 evaluators, completing per-step evaluation forms for all four questions, documenting issues with concrete fixes, and synthesizing findings into a prioritized summary report.
content_id: "5a4b52c7206f4bc4"
tags: [cognitive-walkthrough, process, multi-evaluator, structured, reporting]
---
# Cognitive Walkthrough: Process

## Summary

**One-sentence:** The full structured process for running a cognitive walkthrough: defining prerequisites (persona, task, correct action sequence, interface), assembling 2-4 evaluators, completing per-step evaluation forms for all four questions, documenting issues with concrete fixes, and synthesizing findings into a prioritized summary report.

**One-paragraph:** The full structured process for running a cognitive walkthrough: defining prerequisites (persona, task, correct action sequence, interface), assembling 2-4 evaluators, completing per-step evaluation forms for all four questions, documenting issues with concrete fixes, and synthesizing findings into a prioritized summary report. Lock the action sequence before any evaluation begins — mid-walk changes invalidate per-step JSON.

## Applies If (ALL must hold)

- Running a structured, multi-evaluator cognitive walkthrough where outputs must be produced consistently.
- CI-integrated walkthroughs: every preview deploy of a critical flow (signup, checkout, onboarding) gets an automated walk and the report attached to the PR.
- Cross-evaluator aggregation: two human evaluators + one agent fill forms independently; a reconciler merges results.
- Re-evaluation after fixes — agent re-runs the full process artifact-by-artifact and produces a delta report.

## Skip If (ANY kills it)

- Ad-hoc one-screen reviews — use cog-walk-basics, not the full process. Process overhead isn't worth it.
- When task sequence is not yet stable (changing daily). Lock the action sequence first, then walk.
- Studies where stakeholders need real user voice — process produces inspection findings, not user evidence.
- Multi-app journeys spanning systems the agent can't render (native installer + email + browser) without orchestration.

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

- parent skill: `pro/ux/ux-researcher/`
