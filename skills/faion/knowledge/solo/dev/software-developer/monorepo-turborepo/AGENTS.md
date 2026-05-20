---
slug: monorepo-turborepo
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Turborepo is a high-performance build system for JavaScript/TypeScript monorepos.
content_id: "5c20a5f49e87d519"
tags: [monorepo, turborepo, build-system, task-pipeline, workspace]
---
# Monorepo Setup with Turborepo

## Summary

**One-sentence:** Turborepo is a high-performance build system for JavaScript/TypeScript monorepos.

**One-paragraph:** Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. It provides intelligent caching, parallel task execution, and incremental builds across multiple packages and apps. The core rule: every cacheable task must declare explicit outputs and dependsOn; omitting either causes stale or no-cache builds.

## Applies If (ALL must hold)

- 2+ JS/TS apps sharing UI components, types, or utility packages
- Solo or small team running web + admin + marketing site from one repo with shared lint/format/CI
- Projects where CI build time is dominated by re-running unchanged work
- Microservices in TS/JS where shared types (zod schemas, OpenAPI clients) need a single source of truth

## Skip If (ANY kills it)

- Single app, no shared code — Turbo overhead exceeds benefit
- Polyglot monorepos (Go + TS + Python) — Turbo only orchestrates JS scripts; use Bazel, Pants, or Moon instead
- Projects needing sophisticated dependency graphs (codegen → build → release) — Nx or Bazel scales further
- Teams already on Lerna or Yarn Workspaces with no perf pain — migration cost may not pay back

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

- parent skill: `solo/dev/software-developer/`
