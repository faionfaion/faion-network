---
slug: code-quality-trends
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A snapshot checklist of current quality standards for mainstream stacks (TypeScript 5/React 19/Next.
content_id: "359fa260a527f17a"
tags: [code-quality, standards, linting, type-safety, ci]
---
# Code Quality Trends 2026

## Summary

**One-sentence:** A snapshot checklist of current quality standards for mainstream stacks (TypeScript 5/React 19/Next.

**One-paragraph:** A snapshot checklist of current quality standards for mainstream stacks (TypeScript 5/React 19/Next.js 15, Python 3.12+, Go, Rust) covering linting, type safety, testing coverage targets, performance budgets, and security practices. Treat as a configuration generator and audit driver, not a source of truth — refresh quarterly.

## Applies If (ALL must hold)

- Setting up a new repo: generate lint/format/test/CI configs matched to the detected stack.
- Quarterly tech-debt audit: compare repo against checklist, emit prioritized gap list.
- Onboarding a stack the team hasn't touched in 18+ months — surface what changed.
- Defining CI performance budgets (FCP, API p95 latency, error rate) from the benchmarks table.

## Skip If (ANY kills it)

- Critical stack decisions requiring judgment about team skill, hiring, or vendor lock-in — checklist is descriptive, not normative.
- Late-stage products where a stack switch is prohibitively expensive — high adoption stats don't justify migration.
- Niche stacks (Elixir, Clojure, Zig) — the checklist is mainstream-biased.
- Real-time incident response — performance benchmarks are aspirational, not SLO replacements.

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
