---
slug: monorepo-turborepo
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Turborepo is a high-performance build orchestrator for JavaScript/TypeScript monorepos.
content_id: "5c20a5f49e87d519"
tags: [monorepo, turborepo, pnpm, build-orchestration, typescript]
---
# Monorepo Setup with Turborepo

## Summary

**One-sentence:** Turborepo is a high-performance build orchestrator for JavaScript/TypeScript monorepos.

**One-paragraph:** Turborepo is a high-performance build orchestrator for JavaScript/TypeScript monorepos. Structure code as apps/ and packages/ under pnpm workspaces, declare task dependencies in turbo.json tasks field (v2), and let Turborepo cache and parallelize builds. Internal deps use workspace:*; shared config lives in packages/config.

## Applies If (ALL must hold)

- Bootstrapping a JS/TS monorepo from scratch with multiple apps and shared packages.
- Migrating several npm repos into a single workspace to reduce duplication and improve shared code reuse.
- Adding remote caching to an existing Turborepo or multi-package repo to speed up CI pipelines.
- Standardizing tsconfig, eslint, and prettier across packages via packages/config.
- CI builds taking longer than 2 minutes because unchanged packages rebuild unnecessarily.

## Skip If (ANY kills it)

- Polyglot monorepos that are not JS-dominant (Python + Go + JS) — use Bazel, Pants, or Nx with custom executors instead.
- Tiny single-app projects with only one apps/web — Turborepo overhead is not justified; pnpm workspaces alone suffice.
- Serverless-first projects where each function deploys independently and shared code is minimal — workspace symlinks complicate deployment bundlers.
- Teams without a remote cache strategy — local-only caching gives less than 50% of the benefit; remote cache is mandatory for ROI.

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

- parent skill: `solo/dev/automation-tooling/`
