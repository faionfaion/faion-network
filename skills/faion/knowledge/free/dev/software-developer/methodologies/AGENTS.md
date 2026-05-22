---
slug: methodologies
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a keyword-to-slug dispatch decision (one sibling methodology + its resolved path) by matching the task verb+noun against the named keyword table in this file's content.
content_id: "methodologies-fb11"
complexity: light
produces: report
est_tokens: 2700
tags: [dispatcher, routing, methodologies, keyword]
---
# Methodologies Dispatcher

## Summary

**One-sentence:** Produces a keyword-to-slug dispatch decision (one sibling methodology + its resolved path) by matching the task verb+noun against the named keyword table in this file's content.

**One-paragraph:** A dispatcher index for the software-developer skill. Not a standalone methodology — maps task keywords to canonical sibling methodology folders under `free/dev/software-developer/`. Each sibling contains the full authoritative content; this index only provides a starting routing point. Always hop to the sibling AGENTS.md before implementing anything. Validate agent/methodology names against the actual filesystem before delegating; never use names from historical rows.

**Ефективно для:** routing free-text tasks to the right sibling methodology, building a quick mapping inside the software-developer orchestrator, complementing the `files-reference` catalogue when keywords are clearer than directory grouping.

## Applies If (ALL must hold)

- The task name contains a verb (write, fix, refactor, scaffold) + a noun (handler, test, schema).
- The caller can resolve filesystem paths via Glob/ls.
- The caller is inside the `software-developer` skill scope.

## Skip If (ANY kills it)

- Task contains no recognisable verb+noun pair — use semantic Grep instead.
- Caller wants tier metadata — use the tier-manifest, not this dispatcher.
- Caller already knows the slug — load the sibling directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Free-text task | string | user prompt / ticket |
| Filesystem access | tool capability | runtime env |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[files-reference]]` | Companion catalogue grouped by language; fallback when keyword match fails. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: hop to sibling AGENTS.md, validate against filesystem, return ≤1 slug, never invent. | ~500 |
| `content/02-output-contract.xml` | essential | JSON Schema for dispatch report + valid/invalid examples | ~500 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: stale slug, manual-style usage, no Glob verification | ~500 |
| `content/05-examples.xml` | light | Two worked dispatches | ~400 |
| `content/06-decision-tree.xml` | essential | Root: "Does the task verb+noun match a keyword?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Keyword to slug match | haiku | Lookup table; no reasoning. |
| Verification + escalation | sonnet | Short natural-language message. |

## Templates

| File | Purpose |
|------|---------|
| (none) | This dispatcher emits JSON; no templates. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodologies.py` | Validates dispatch report shape and resolves the picked slug on disk. | After dispatcher emits, before downstream load. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[files-reference]]` — language-grouped catalogue
- `[[language-framework-guide]]` — stack-level dispatcher

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: keyword match exists yes/no, slug resolves on disk yes/no.
