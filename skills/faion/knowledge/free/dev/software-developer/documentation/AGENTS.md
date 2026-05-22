---
slug: documentation
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Convention for writing AI-readable directory context files: CLAUDE.
content_id: "8932853683be833c"
tags: [documentation, claude-md, agents-md, convention, routing]
---
# CLAUDE.md / AGENTS.md Documentation

## Summary

**One-sentence:** Convention for writing AI-readable directory context files: CLAUDE.

**One-paragraph:** Convention for writing AI-readable directory context files: CLAUDE.md (single line: @AGENTS.md) and AGENTS.md (20-80 lines covering purpose, file table, key types, commands, gotchas). Required in every directory with source code — not just repo roots but also subpackages, module folders, test dirs.

## Applies If (ALL must hold)

- Creating a new directory with code: add CLAUDE.md + AGENTS.md before any other file.
- Onboarding an agent to an unfamiliar module — agent reads AGENTS.md to route, then loads specific files.
- After a significant refactor: regenerate AGENTS.md so future context loads stay accurate.
- Multi-agent workspaces where each tool reads a different filename.
- Repos with many sub-packages where loading the whole tree blows context budget.

## Skip If (ANY kills it)

- Tiny one-file scripts — a README is sufficient.
- Generated / vendored code (node_modules/, dist/) — never document these.
- Highly volatile prototypes where structure changes daily — document after dust settles.
- Directories that are pure data (assets, fixtures) without logic.

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

- parent skill: `free/dev/software-developer/`
