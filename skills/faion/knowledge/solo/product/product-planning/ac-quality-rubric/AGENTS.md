---
slug: ac-quality-rubric
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A scoring rubric for acceptance criteria that flags weak ACs before sprint planning, with a fix-pattern table for each weakness type.
content_id: "30f8c91a7a7d4522"
tags: [product, acceptance-criteria, ac, dor, scrum, quality, bdd]
---

# Acceptance Criteria Quality Rubric

## Summary

**One-sentence:** A 7-dimension rubric (testability, observability, scope, precondition, postcondition, edge-case coverage, BDD form) that scores each acceptance criterion 0-2 per dimension; criteria scoring below 10/14 are sent back for rewrite before sprint commitment.

**One-paragraph:** Acceptance criteria are the contract between PM, dev, and QA. Weak ACs are the lever for shipping speed — they cause mid-sprint clarification rounds, "feature works but not what was asked" rework, and QA test gaps. Mechanism: score each AC against 7 dimensions (each 0/1/2), reject below 10/14, and provide a fix-pattern table so authors learn the rewrite shape. Primary output: a rubric score per AC + a rewrite for any failing AC + a refusal to accept the story into sprint until all ACs score ≥ 10.

## Applies If (ALL must hold)

- team uses acceptance criteria as the sprint-commit gate (Scrum / Kanban-with-AC)
- backlog has stories awaiting refinement OR sprint-planning queue is forming
- product owner / PM is the AC author (or final approver)
- team has experienced one or more "feature works but wasn't what was asked" reworks in the last 90 days

## Skip If (ANY kills it)

- pure exploratory / spike work — ACs are wrong tool; use spike timebox + outcome write-up instead
- solo dev who is also product owner — internal consistency check is faster than formal rubric
- production-incident hotfix — rubric overhead exceeds defect cost; ship with minimal AC + retro
- team uses outcome-based pull (Shape Up) — pitch quality rubric is the correct artifact instead

## Prerequisites

- existing ACs in some form (acceptance text on Jira / Linear / GitHub story)
- AC author available for rewrite if rubric flags an AC
- team agreed that stories with failing ACs do not enter sprint
- "definition of done" exists separately — ACs are pre-build contract, DoD is post-build verification

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/sdd-planning/definition-of-ready-template` | DoR includes "ACs pass quality rubric"; consume the DoR gate spec |
| `pro/ba/business-analyst/acceptance-criteria-writing` | Original AC writing patterns (Given-When-Then etc.); rubric scores against these |
| `solo/product/product-planning/story-slicing` | Slicing produces multiple thin stories each with own ACs; rubric runs per story |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 7-dimension-scoring, 10-of-14-threshold, no-acceptance-without-rewrite, fix-pattern-required, AC-not-implementation | ~1000 |
| `content/02-output-contract.xml` | essential | Per-AC score record schema + rewrite contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (gold-plated rubric, score inflation, implementation-creep, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_dimension_score` | sonnet | Per-AC evaluation, bounded judgment |
| `failure_pattern_diagnosis` | sonnet | Match weak AC against fix-pattern table |
| `rewrite_proposal` | sonnet | Generate rewrite candidate following fix pattern |
| `story_level_aggregation` | haiku | Sum scores, output pass/needs-rewrite |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-score-record.json` | JSON Schema for one AC's rubric output |
| `templates/fix-pattern-table.md` | Lookup: weakness signal -> rewrite shape |
| `templates/rubric-card.md` | Printable rubric card for PM / BA workshops |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-ac.py` | Runs rubric on a story's ACs, returns per-AC + aggregate score | At backlog refinement, before sprint commit |
| `scripts/rubric-history.py` | Tracks team's AC quality over time; flags trend regressions | Monthly retro input |

## Related

- parent skill: `solo/product/product-planning/`
- peer methodologies: `story-slicing`, `definition-of-ready-template`, `inv-est-criteria`
- external: [Cohn — User Stories Applied](https://www.mountaingoatsoftware.com/books/user-stories-applied) · [SpecFlow BDD guide](https://specflow.org/learn/) · [Atlassian AC examples](https://www.atlassian.com/agile/project-management/user-stories)
