---
slug: documentation
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Create AI-readable documentation pairs for every code directory: CLAUDE.
content_id: "8932853683be833c"
tags: [documentation, ai-readability, agents-md, routing, code-organization]
---
# Documentation (AGENTS.md and CLAUDE.md)

## Summary

**One-sentence:** Create AI-readable documentation pairs for every code directory: CLAUDE.

**One-paragraph:** Create AI-readable documentation pairs for every code directory: CLAUDE.md (one line: @AGENTS.md) and AGENTS.md (20-80 lines describing what the dir is, its files, entry points, and gotchas). Without this pair, agents load no context and scan files blindly, wasting tokens and hallucinating structure.

## Applies If (ALL must hold)

- Bootstrapping AI-readable docs in a new repo, sub-package, or refactored directory.
- After a refactor where the file tree changed and existing AGENTS.md tables are stale.
- Multi-repo monorepos: each package needs its own AGENTS.md per the project convention.
- Legacy codebases with only a top-level README — rolling out per-module coverage.

## Skip If (ANY kills it)

- Repos under ~200 lines with one obvious entry point — a README suffices.
- Generated/derived directories (dist/, build/, node_modules/) — docs just repeat tooling output.
- Short-lived experiments where the doc rots faster than the code iterates.
- Public-facing user docs (Docusaurus/Mintlify) — this methodology targets AI readers, not customers.

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

- parent skill: `free/dev/code-quality/`
