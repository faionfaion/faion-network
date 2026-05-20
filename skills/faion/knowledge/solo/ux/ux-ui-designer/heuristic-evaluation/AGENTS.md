---
slug: heuristic-evaluation
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured usability inspection method where 3-5 evaluators independently review an interface against Nielsen's 10 heuristics and rate each issue on a 0-4 severity scale (0=not a problem, 4=catastrophic).
content_id: "432b0a5968c469ed"
tags: [usability-testing, heuristic-evaluation, expert-review, quality-assurance, severit-scale]
---
# Heuristic Evaluation

## Summary

**One-sentence:** A structured usability inspection method where 3-5 evaluators independently review an interface against Nielsen's 10 heuristics and rate each issue on a 0-4 severity scale (0=not a problem, 4=catastrophic).

**One-paragraph:** A structured usability inspection method where 3-5 evaluators independently review an interface against Nielsen's 10 heuristics and rate each issue on a 0-4 severity scale (0=not a problem, 4=catastrophic). Evaluators work independently first, then findings are compiled and deduplicated. One pass per heuristic yields ~3x more findings than a single omnibus pass. Severity 4 blocks release; severity 3 is sprint-level; severity 1-2 goes to polish backlog.

## Applies If (ALL must hold)

- Before a usability test — eliminate obvious violations so testing resources address real user behavior
- When no user research budget is available — gives actionable findings at near-zero cost
- After a design sprint or major redesign — rapid expert review before development handoff
- Code review for UI components — catching violations in PRs prevents regressions
- Competitive analysis: apply the same heuristics to competitors to score relative quality

## Skip If (ANY kills it)

- As a replacement for usability testing — finds expert-visible violations, not real user struggles with domain tasks
- After launch as the sole quality gate — too late for design changes; use for iterative improvements
- When quantitative data is needed to justify decisions — heuristic evaluation produces qualitative expert opinions
- On expert-user products where violations are worked around via muscle memory — disrupting their efficiency is worse

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

- parent skill: `solo/ux/ux-ui-designer/`
