---
slug: ai-diff-size-discipline
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Caps AI-authored diffs to a reviewable size by emitting a per-PR rubric — lines-touched, files-touched, semantic-units, and a split plan if any cap is breached.
content_id: "dd1e2c9293f311b7"
complexity: medium
produces: rubric
est_tokens: 4000
tags: [ai-pair-coding, diff-size, code-review, discipline, claude-code]
---
# AI Diff Size Discipline

## Summary

**One-sentence:** Caps AI-authored diffs to a reviewable size by emitting a per-PR rubric — lines-touched, files-touched, semantic-units, and a split plan if any cap is breached.

**One-paragraph:** Large AI diffs hide bugs because reviewers cannot hold them in mind; small diffs hide nothing. This methodology emits a per-PR rubric scoring the diff against three caps (LOC, files, semantic units) and — when any cap is breached — a split-plan that decomposes the diff into shippable slices. Default caps: <= 200 LOC excluding tests, <= 8 files, <= 1 semantic unit (1 feature OR 1 refactor, never both).

**Ефективно для:**

- Solo dev using Claude Code / Cursor on a feature larger than one sitting.
- Code-review gate that catches AI "helpful" sprawl before it lands on main.
- Refactor + feature combo where the AI bundled both into one diff.
- Onboarding a new contributor whose diffs need a size rail.

## Applies If (ALL must hold)

- PR was at least partly authored by an AI pair (Claude Code / Cursor / Copilot).
- Reviewer is a human (not auto-merge).
- Repo has a small set of explicit size caps the team agreed on.
- PR is not a one-time large migration or generated-code dump.

## Skip If (ANY kills it)

- Generated-code update (codegen / proto) — split makes no sense.
- Single-file lockfile bump.
- Pure documentation reorganisation (no code semantics).
- Emergency hotfix where review delay costs more than diff size.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Raw diff (git diff) | unified diff | PR / branch |
| Repo caps config | JSON or YAML | team-agreed defaults |
| PR description | markdown | author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-pair-coding-prompt-patterns]] | Prompt patterns produce the AI diff this rubric scores. |
| [[ai-generated-test-validation]] | Both run together at PR gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (LOC cap, file cap, single-unit, split plan, override gate) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for diff-rubric + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: refactor-and-feature, opaque-rename, no-tests, scope-creep | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (measure → score → verdict → split-plan → enforce) | 700 |
| `content/05-examples.xml` | essential | Worked example: 800 LOC AI diff split into 3 PRs | 600 |
| `content/06-decision-tree.xml` | essential | Routes by LOC + files + unit-count | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ai_diff_size_discipline_measure` | haiku | Mechanical line+file count. |
| `ai_diff_size_discipline_classify_units` | sonnet | Semantic-unit decomposition needs judgement. |
| `ai_diff_size_discipline_split_plan` | sonnet | Slice ordering with dependency analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the diff-rubric artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in diff-rubric for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-diff-size-discipline.py` | Validate ai-diff-size-discipline artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[ai-pair-coding-prompt-patterns]]
- [[ai-generated-test-validation]]
- [[exploratory-testing-charters]]
- [[feature-flag-cleanup-discipline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) LOC &lt;= 200, (b) files &lt;= 8, (c) semantic_units == 1. Any breach drives verdict=split; the rubric must then carry a split-plan. Every leaf references a rule in `01-core-rules.xml`.
