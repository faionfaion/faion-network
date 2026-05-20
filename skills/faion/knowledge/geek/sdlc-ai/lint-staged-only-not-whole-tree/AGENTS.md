---
slug: lint-staged-only-not-whole-tree
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every linter and formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repository tree.
content_id: "9ac00e789b8e6477"
tags: [pre-commit, lint-staged, lefthook, hooks, staged-files]
---
# Pre-Commit Linters MUST Run on Staged Files Only

## Summary

**One-sentence:** Every linter and formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repository tree.

**One-paragraph:** Every linter and formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repository tree. Use pre-commit's default pass_filenames: true (the framework already passes the staged list as args), lefthook's {staged_files} template, or lint-staged for husky setups. NEVER call eslint ., ruff check ., biome check ., prettier --write ., or mypy . from a pre-commit hook — those rewrite or report on unrelated files, balloon the diff, drag the hook above one second, and push developers and agents toward --no-verify. CI runs the whole-tree variant exactly once per PR as the final pre-merge gate.

## Applies If (ALL must hold)

- Always — every pre-commit hook in every framework MUST be staged-scoped.
- Especially in monorepos where any hook will encounter thousands of files.
- When wrapping a custom command in a `local` hook (forwarding $@ is mandatory).
- When migrating a husky setup off `npm run lint` invocations toward lint-staged.

## Skip If (ANY kills it)

- The CI pre-merge gate — that runs whole-tree by design as the final defense.
- One-off "format the entire repo" maintenance commits scheduled as their own PR — these run outside the hook.
- Tools that fundamentally need the whole project graph (e.g., tsc -p) — these MAY run scoped to a project but never to a single file; use a separate hook with pass_filenames: false.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
