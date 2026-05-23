---
slug: weekly-branch-hygiene-checklist
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Friday 30-minute branch-hygiene checklist — rebase, squash, changelog, stale-branch sweep — closing the gap between trunk-based principle and weekly ritual.
content_id: "1a6ebdb6729bd21c"
complexity: light
produces: checklist
est_tokens: 4200
tags: ["branch-hygiene", "trunk-based", "rebase", "changelog", "ritual"]
---
# Weekly Branch Hygiene Checklist

## Summary

**One-sentence:** Generates a Friday 30-minute branch-hygiene checklist — rebase, squash, changelog, stale-branch sweep — closing the gap between trunk-based principle and weekly ritual.

**One-paragraph:** Generates a Friday 30-minute branch-hygiene checklist — rebase, squash, changelog, stale-branch sweep — closing the gap between trunk-based principle and weekly ritual.

**Ефективно для:**

- Solo developer who accumulates branches mid-week.
- Pre-merge Friday cleanup before weekend.
- Trunk-based-development team that lost discipline.

## Applies If (ALL must hold)

- Repo uses trunk-based or short-lived feature branches.
- Developer commits to a weekly cadence (≥1 day/week).
- Changelog file exists OR will be created.
- Developer has rebase + squash authority.

## Skip If (ANY kills it)

- Long-lived release branches mandated by org — cadence does not apply.
- Greenfield prototype with no PRs.
- Single-commit-per-week pace — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Branch inventory | git | git branch -a |
| Changelog path | path | CHANGELOG.md |
| Stale threshold | days | default 14 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| timeboxed-refactor-session-template | Hygiene block uses the same timebox discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-fixed-day-and-duration, r2-rebase-onto-main, r3-stale-sweep, r4-changelog-entry, r5-named-owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Weekly Branch Hygiene Checklist artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: cadence-drift, merge-commit-cleanup, stale-forever | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-weekly-branch-hygiene-checklist` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-weekly-branch-hygiene-checklist` | sonnet | Bounded structural check against the output contract. |
| `review-weekly-branch-hygiene-checklist` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-branch-hygiene-checklist.json` | JSON skeleton matching the output contract. |
| `templates/weekly-branch-hygiene-checklist.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-branch-hygiene-checklist.py` | Validate Weekly Branch Hygiene Checklist output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[timeboxed-refactor-session-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
