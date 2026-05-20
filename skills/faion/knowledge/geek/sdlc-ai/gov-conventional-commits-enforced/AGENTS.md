---
slug: gov-conventional-commits-enforced
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every repo enforces Conventional Commits 1.
content_id: "bdcf2ae3e9a30c8d"
tags: [governance, conventional-commits, commitlint, changelog, semver]
---
# Conventional Commits Enforced at the Hook

## Summary

**One-sentence:** Every repo enforces Conventional Commits 1.

**One-paragraph:** Every repo enforces Conventional Commits 1.0.0 (`feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `style`, `revert`; optional scope; optional `!` for breaking; mandatory `BREAKING CHANGE:` footer when `!` is used) via a `commitlint` `commit-msg` hook plus a CI PR-title check. The CHANGELOG, semver bump, and release notes are derived deterministically from the log; agents never freeform commit subjects. Non-conformant messages are rejected at hook time, before they reach the remote.

## Applies If (ALL must hold)

- Any team repo that produces releases (libraries, services with semver, monorepos with independent package versions).
- Repos where AI agents create commits autonomously and a human curator does not edit every subject line.
- Projects with downstream consumers expecting semver-correct changelogs (npm, PyPI, NuGet, Maven Central, Helm charts).
- Monorepos using `release-please` / `semantic-release` / `changesets` — these tools refuse to operate without conformant messages.

## Skip If (ANY kills it)

- Single-developer scratch repos and throwaway prototypes — overhead exceeds benefit.
- Mirror / vendored repos where commits are imported verbatim from upstream.
- Migration-in-progress repos where rewriting historical messages is out of scope; turn it on at a fresh tag and skip backfill.
- Repos that intentionally use squash-on-merge with auto-generated subjects from PR titles — gate the PR title instead.

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
