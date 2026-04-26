# WBS Creation

## Summary

Work Breakdown Structure (WBS) creation decomposes the total project scope into deliverable-oriented, hierarchically numbered work packages that are estimable (8-80 hours), assignable to one owner, and measurable against a clear completion criterion. Names at every level are nouns (deliverables), never verbs (activities). The 100% rule requires that every work package rolls up completely to its parent.

## Why

Without a WBS, estimates are guesses and dependencies are invisible until they block progress. Deliverable-oriented decomposition forces the team to answer "what will be produced?" before "how will we produce it?", which surfaces scope gaps and prevents activity-focused planning that omits unassigned outputs. The WBS dictionary transforms numbered IDs into testable acceptance criteria.

## When To Use

- New projects where scope is fixed enough to decompose into deliverables (more than four weeks of work).
- Fixed-bid proposals where each work package needs an hours/cost line for the estimate.
- Programs requiring a contractual scope baseline with WBS IDs for traceability.
- Migration or cutover projects where a missing deliverable is expensive.

## When NOT To Use

- Pure-Scrum backlog work where the product backlog serves the same role.
- Exploratory R&D — the deliverables are unknown before the work begins.
- Single-week tasks — a checklist is faster.
- Continuous operations or service catalog work — use the service catalog instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | 100% rule, deliverable orientation, hierarchy levels, work-package criteria |
| `content/02-rules.xml` | Rules for naming discipline, depth limits, dictionary requirements, and agentic WBS authoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md` | WBS outline template in Markdown outline format |
| `templates/wbs-dictionary-entry.md` | WBS dictionary entry template for a single work package |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/wbs_lint.py` | Lints a YAML WBS for verb-led names, depth violations, and missing PM branch |
