---
slug: lang-php-phpstan9-psalm-taint
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run two static analyzers in CI for every PHP project where AI agents author code: PHPStan at level 9 (or 10 for libraries) for type strictness, and Psalm with --taint-analysis for inter-procedural data-flow checks (SQLi, XSS, command injection).
content_id: "000ed7a59aaeb4c1"
tags: [php, phpstan, psalm, static-analysis, taint-analysis]
---
# PHP Dual Gate: PHPStan Level 9 + Psalm Taint Analysis

## Summary

**One-sentence:** Run two static analyzers in CI for every PHP project where AI agents author code: PHPStan at level 9 (or 10 for libraries) for type strictness, and Psalm with --taint-analysis for inter-procedural data-flow checks (SQLi, XSS, command injection).

**One-paragraph:** Run two static analyzers in CI for every PHP project where AI agents author code: PHPStan at level 9 (or 10 for libraries) for type strictness, and Psalm with --taint-analysis for inter-procedural data-flow checks (SQLi, XSS, command injection). Both must report green before merge.

## Applies If (ALL must hold)

- Symfony, Laravel, Drupal, or vanilla PHP services with agent contributors.
- Projects with web-facing controllers, ORM query builders, file uploads, shell command construction.
- Codebases ratcheting up type strictness (start L5, increment per release; pin L9 once green).
- Library packages targeting Packagist — level 10 is feasible because there is no framework noise.

## Skip If (ANY kills it)

- Greenfield prototypes under ~1 KLOC where the bootstrap cost dominates value.
- Pure CLI scripts with no external input — Psalm's taint pass produces no signal.
- Legacy codebases where setting L9 day one would mark thousands of files as failing — phase from L5 to L7 to L9 with the baseline file.

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
