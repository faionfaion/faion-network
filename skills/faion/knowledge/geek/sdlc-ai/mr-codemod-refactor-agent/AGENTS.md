---
slug: mr-codemod-refactor-agent
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cross-cutting refactors (Angular 17→20, AI SDK 5→6, rename User.
content_id: "0f03ab3e40964aa8"
tags: [codemod, refactor, ast, multi-agent, pull-request]
---
# Codemod-First Refactor Agent

## Summary

**One-sentence:** Cross-cutting refactors (Angular 17→20, AI SDK 5→6, rename User.

**One-paragraph:** Cross-cutting refactors (Angular 17→20, AI SDK 5→6, rename User.email→User.contact) are codemods, not chat conversations. Use AST-aware tools (jscodeshift, ts-morph, libcst, semgrep, codemod.com / Hypermod) to do the deterministic 95% of edits, then let an LLM finish the long-tail (string templates, tests, docstrings, README snippets) that AST cannot reach. Open ONE PR per logical group of changes — not one per file. Multi-agent stacks (Architect → Migration → Validator) generate the PR with summary plus risk notes.

## Applies If (ALL must hold)

- Framework upgrades that ship breaking renames (Angular, React, Next.js, Vue, AI SDK).
- API renames or deprecation removals across >100 call-sites.
- Lint-rule rollouts where every existing violation must be auto-fixed (TS strict mode flip, ESLint rule).
- Schema migrations where the field rename touches code, tests, fixtures, and docs in lockstep.

## Skip If (ANY kills it)

- Small renames (<20 sites) — IDE rename refactor is faster and safer; codemod overhead is not justified.
- Semantic refactors where the type signature stays but the BEHAVIOUR changes — codemods don't see behaviour.
- Refactors that require staged rollout across multiple deploys — split into staged PRs first.
- Generated code where the source-of-truth is not the file being changed.

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
