---
slug: monorepo-turborepo
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Run a JS/TS monorepo with Turborepo: pnpm workspaces, pinned versions, declared task pipeline, content-hash cache, and remote cache for CI.
content_id: "913c059de626fb0c"
complexity: medium
produces: config
est_tokens: 4000
tags: [monorepo, turborepo, build-system, task-pipeline, workspace]
---
# Monorepo with Turborepo

## Summary

**One-sentence:** Run a JS/TS monorepo with Turborepo: pnpm workspaces, pinned versions, declared task pipeline, content-hash cache, and remote cache for CI.

**One-paragraph:** Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. Pnpm workspaces own dependency management; turbo.json declares the task pipeline (build → test → lint) with explicit dependsOn edges; content-hash cache makes incremental builds deterministic; remote cache (Vercel Remote Cache or self-hosted) shares hits across CI workers. Output is the workspace + turbo.json + CI integration.

**Ефективно для:**

- Multi-package JS/TS repos (web + api + shared libs).
- Speeding up CI by sharing cached results across PRs.
- Standardising scripts (build/test/lint) across packages.
- Replacing ad-hoc lerna or npm-workspaces setups.

## Applies If (ALL must hold)

- Monorepo has >=3 packages (or apps + at least 1 shared lib).
- Stack is JS/TS with Node >=18.
- Team uses pnpm (or willing to migrate from npm/yarn).
- CI runs the same task pipeline across PRs (caching has payoff).

## Skip If (ANY kills it)

- Single-package repo — Turborepo is overhead without payoff.
- Polyglot monorepo where build owns multiple languages — use Bazel/Nx with language plugins.
- Tiny script repo where caching benefit < setup cost.
- Project already on Nx and migrating would cost more than the benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Package inventory: apps + libs + ownership | table | tech-lead |
| Pnpm version + workspace layout chosen | config | platform |
| Task graph: which task depends on which (build → test ordering) | ADR | tech-lead |
| Remote cache provider (Vercel Remote Cache or self-hosted) + token | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[frontend-design]] | Apps may consume the design tokens lib. |
| [[nodejs-service-layer]] | Service apps follow the layered conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (pnpm workspaces, turbo.json explicit pipeline, pinned versions, cache outputs declared, remote cache in CI, no top-level scripts that bypass turbo) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for monorepo config spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: workspace init → turbo.json → pin versions → cache outputs → remote cache CI | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workspace_layout` | sonnet | Mechanical: pnpm-workspace.yaml + package layout. |
| `pipeline_authoring` | opus | Task graph design (build/test/lint dependencies) needs synthesis. |
| `cache_config` | sonnet | Declare outputs per task; verify cache hit rate. |
| `remote_cache_ci` | sonnet | Wire TURBO_TOKEN + TURBO_TEAM env vars in CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pnpm-workspace.yaml` | pnpm workspace declaration |
| `templates/turbo.json` | Turborepo pipeline config with cached outputs |
| `templates/tsconfig-base.json` | Shared tsconfig referenced by package tsconfigs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monorepo-turborepo.py` | Validate monorepo config spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[nodejs-service-layer]]
- [[nextjs-app-router]]
- [[frontend-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps repo size, language scope, and caching payoff to a rule from `01-core-rules.xml`, telling the agent whether to apply Turborepo or skip for single-package / polyglot cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
