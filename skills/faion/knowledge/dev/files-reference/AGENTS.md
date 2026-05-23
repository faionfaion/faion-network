# Software Developer Files Reference

## Summary

**One-sentence:** Produces a verified routing decision (one or two methodology slugs + resolved absolute paths) for a free-text software-developer task by reading the per-language section of the catalog and gating each candidate through a Glob lookup.

**One-paragraph:** The `software-developer` skill contains 200+ methodology entries across many languages. A grouped catalog lets an agent identify the topical section (e.g. "Go") in one read, then resolve the actual subfolder path via `Glob`, rather than scanning the entire tree. Faster routing, lower context cost, fewer hallucinated paths. The catalog itself is name-based and may be stale — every selected slug MUST be re-validated against the filesystem with `Glob` before downstream loading.

**Ефективно для:** first-pass routing inside the `software-developer` orchestrator, building documentation sidebars, validating that referenced methodology folders exist before dispatching a sub-agent task.

## Applies If (ALL must hold)

- The caller has a free-text task and needs to pick a methodology folder, not browse all of them.
- The caller can run `Glob` (or shell `ls`) to verify candidate paths before loading.
- The task language/area is one of the catalog's named sections (python, go, javascript, testing, frontend, dev-practices, etc.).

## Skip If (ANY kills it)

- Semantic search needed ("how do I handle errors?") — use `Grep` over actual content, not name-based catalog.
- Caller wants an authoritative tier map — trust the directory tree, not this catalog.
- Bulk dumping the full catalog into a sub-agent prompt — too large; filter to one section.
- Catalog row appears stale (path missing on disk) — escalate, do not auto-edit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Free-text task | string ("Write a Gin handler") | user prompt or PM ticket |
| Tier of caller | one of free/solo/pro/geek | session context |
| Filesystem access for Glob | tool capability | runtime env |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[methodologies]]` | sibling dispatcher providing the keyword to slug mapping; this file backstops it with the catalog. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one section per task, verify with Glob, never invent paths, escalate on stale, no full-catalog dumps | ~500 |
| `content/02-output-contract.xml` | essential | JSON Schema for the candidates report + valid/invalid examples | ~500 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: invented slugs, no Glob verification, full-catalog dump, semantic-search misuse | ~500 |
| `content/05-examples.xml` | light | Two worked routing reports | ~500 |
| `content/06-decision-tree.xml` | essential | Root question on whether task maps to one section | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Section selection + candidate slug picking | haiku | Pure pattern match; no reasoning depth needed. |
| Stale-row escalation message | sonnet | Needs a short natural-language note. |

## Templates

| File | Purpose |
|------|---------|
| (none) | This methodology emits a JSON report; templates not needed. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-files-reference.py` | Validates that a candidates report matches the output schema and each path resolves on disk. | After the routing agent emits a report, before downstream load. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[methodologies]]` — keyword-based dispatcher (companion to this catalog)
- `[[language-framework-guide]]` — stack selection guidance once the routing is done

## Decision tree

The decision tree at `content/06-decision-tree.xml` first checks whether the task's language/area maps to one named section; if yes, pick at most 2 slugs and verify each with Glob; otherwise escalate to semantic search.
