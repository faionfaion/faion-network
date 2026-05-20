---
slug: sprint-goal-formula
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Compact three-part sprint-goal formula (outcome + boundary + measure) that produces a single sentence the team can recite, used to filter scope additions and to grade the sprint at review.
content_id: "c32c46822cc22305"
tags: [project-manager, sprint-planning, sprint-goal, scrum, solo-pm]
---
# Sprint Goal Formula

## Summary

**One-sentence:** A three-part formula — `outcome + boundary + measure` — that compresses a sprint into one sentence the team can recite, then uses to filter mid-sprint scope additions and grade the sprint review.

**One-paragraph:** Most teams ship sprints with a goal that is either missing ("clear the backlog") or unfalsifiable ("improve checkout"). This methodology pins the goal to a single sentence built from three required parts: an outcome (verb + user/system change), a boundary (scope edge — what is in/out), and a measure (a verifiable signal that determines done). Mid-sprint, any new request is graded against the goal: if it advances the outcome inside the boundary, it can be considered; otherwise it goes to next sprint. At sprint review, the measure is the pass/fail check — no narrative grading. Replaces the soft "did we have a good sprint?" question with a binary answer the PM can defend.

## Applies If (ALL must hold)

- Team works in fixed-cadence sprints (1-3 weeks).
- PM (or facilitator) leads sprint planning end-to-end.
- A single team works on the sprint backlog — not a multi-team commitment.
- Team has a backlog of >5 candidate items so a goal is needed to choose between them.

## Skip If (ANY kills it)

- Continuous-flow / Kanban — there are no sprint boundaries to set a goal around.
- Single-developer solo project where the dev IS the user — use `tiny-bets-quarterly-cadence` instead.
- Hard contractual sprint scope (every line item is mandatory) — the goal cannot filter, so the formula adds no value.
- Sprint is purely operational (incidents, support) with no outcome to commit to.

## Prerequisites

- Refined backlog with at least 3 candidate items that share a thematic outcome.
- One business-side stakeholder available to confirm the proposed outcome.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/` | Sprint planning ceremony baseline. |
| `pro/pm/pm-agile/` | Agile ceremony cadence and definitions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: three required parts, single-sentence cap, scope-filter use, review-grading binary, no-multi-goal. | ~900 |

## Related

- parent skill: `solo/pm/project-manager/`
- peer: `sprint-goal-one-liner-template`, `retro-facilitation-multistyle`, `async-standup-methodology`
- external: Scrum Guide 2020 §Sprint Goal
