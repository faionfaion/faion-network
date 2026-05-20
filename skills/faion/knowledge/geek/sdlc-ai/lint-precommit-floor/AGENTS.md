---
slug: lint-precommit-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every repository with code MUST install a pre-commit framework that runs format, lint, secret-scan and type-check hooks before a commit is created — never afterward.
content_id: "13e48fc58cfe4e28"
tags: [lint, pre-commit, lefthook, husky, git-hooks]
---
# Pre-Commit Hooks as the Non-Negotiable Merge Floor

## Summary

**One-sentence:** Every repository with code MUST install a pre-commit framework that runs format, lint, secret-scan and type-check hooks before a commit is created — never afterward.

**One-paragraph:** Every repository with code MUST install a pre-commit framework that runs format, lint, secret-scan and type-check hooks before a commit is created — never afterward. The framework is pre-commit (Python, broadest plug-in ecosystem) for polyglot repositories, lefthook (Go, parallel) for monorepos with throughput pressure, or husky (Node) for pure JavaScript stacks. AI agents NEVER bypass with --no-verify; on any hook failure they read the output, fix the root cause, and re-stage. The list of installed hooks is documented in the repository AGENTS.md so the agent sees the contract before it writes the first line.

## Applies If (ALL must hold)

- Every repository that contains code, including throwaway prototypes that may grow.
- Polyglot repositories where multiple language linters need consistent invocation (pre-commit or lefthook).
- Monorepos with parallel hook execution requirements (lefthook).
- Teams using AI coding agents — the hook list is the agent's compile-time contract.

## Skip If (ANY kills it)

- Single-file gist repositories with no merge workflow — overhead exceeds the benefit.
- Read-only or archived repositories — no commits arrive that the hook could gate.
- Documentation-only repositories with no executable artifacts — a markdownlint hook still helps but the framework choice is overkill if there is one file.

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
