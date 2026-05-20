---
slug: cog-walk-basics
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A usability inspection method where evaluators step through a task from a first-time user's perspective, answering four questions per step: (1) Will the user try to achieve the right effect? (2) Will they notice the correct action? (3) Will they associate the action with the desired effect? (4) Will they see that progress is being made? Designed specifically to expose learnability failures before user testing.
content_id: "1aa71d897cb9dfe0"
tags: [cognitive-walkthrough, usability-inspection, learnability, first-time-user, evaluation]
---
# Cognitive Walkthrough: Basics

## Summary

**One-sentence:** A usability inspection method where evaluators step through a task from a first-time user's perspective, answering four questions per step: (1) Will the user try to achieve the right effect? (2) Will they notice the correct action? (3) Will they associate the action with the desired effect? (4) Will they see that progress is being made? Designed specifically to expose learnability failures before user testing.

**One-paragraph:** A usability inspection method where evaluators step through a task from a first-time user's perspective, answering four questions per step: (1) Will the user try to achieve the right effect? (2) Will they notice the correct action? (3) Will they associate the action with the desired effect? (4) Will they see that progress is being made? Designed specifically to expose learnability failures before user testing.

## Applies If (ALL must hold)

- Pre-launch usability inspection of an onboarding flow, signup, or first-run experience where no users are available yet.
- Evaluating clickable prototypes (Figma, Framer, deployed staging) for learnability before investing in moderated usability testing.
- Reviewing AI-generated UI from a design-to-code tool against the four-question framework before merging to main.
- Onboarding-flow regressions in CI: a vision-capable agent walks the latest preview build and flags new Q1/Q2/Q3/Q4 failures.

## Skip If (ANY kills it)

- Expert-user efficiency tasks (power-user shortcuts, dashboards). Use heuristic evaluation or quantitative testing.
- Highly subjective aesthetic decisions; the four questions don't catch visual hierarchy issues well.
- When you have real users available — actual usability testing always beats inspection.
- Static brand/marketing pages with no task flow — there are no "steps" to walk through.

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
