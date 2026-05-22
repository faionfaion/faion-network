---
slug: javascript-modern
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Configures a modern JS/TS stack: TypeScript strict, named exports, pnpm, ESLint flat config, code-placement rules for Node 22 / Bun / browsers.
content_id: "2576809c69880eb1"
complexity: medium
produces: config
est_tokens: 3700
tags: [typescript, eslint-flat, pnpm, modern-js, strict-mode]
---
# Modern JS/TS

## Summary

**One-sentence:** Emits a modern JS/TS project config bundle (tsconfig strict, eslint.config.js flat, pnpm-lock) with explicit code-placement rules per runtime target.

**One-paragraph:** JS/TS best practices rotate fast: ESLint 9 dropped .eslintrc, pnpm replaced npm for monorepos, named exports replaced default exports, and TypeScript strict mode became table stakes. This methodology emits a config bundle (tsconfig + eslint flat config + package.json scripts + pnpm-workspace.yaml when applicable) tied to the chosen runtime (Node 22 / Bun / browser). Output is a versioned config artefact that can be landed in one PR; updates quarterly via code-quality-trends.

**Ефективно для:**

- Net-new JS/TS проекти: один config-bundle замість 8-ми тікетів-апгрейдів.
- Старі проекти на ESLint 8.x: migration to flat config за один PR.
- Monorepo: pnpm + workspaces один раз, потім працює.
- Mixed-runtime org (Node + Bun + browser): code-placement rules не дозволяють Node-only API в browser-bundle.

## Applies If (ALL must hold)

- Stack is JS or TS.
- Target runtime is one of: Node 22, Bun, browser, edge.
- Owner can land the config PR.

## Skip If (ANY kills it)

- Stack is locked to Node 16 / pre-ESM tooling — modern config breaks.
- Enterprise-managed config (parent repo dictates) — defer.
- End-of-life project.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo + package.json | path | repo root |
| Target runtime | enum | owner decision |
| Existing tsconfig / eslint | files | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typescript-strict, eslint-flat, named-exports, pnpm-for-monorepo, runtime-targeted-placement | 1000 |
| `content/02-output-contract.xml` | essential | Schema for config bundle artefact | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: default-export-everywhere, eslintrc-still-around, node-api-in-browser-code | 700 |
| `content/04-procedure.xml` | essential | 5-step migration procedure | 700 |
| `content/06-decision-tree.xml` | essential | Runtime + monorepo tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit_current` | haiku | Read existing configs. |
| `draft_bundle` | sonnet | Per-stack customisation. |
| `estimate_blast_radius` | haiku | Count of files affected by strict flags. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.strict.json` | Strict tsconfig baseline |
| `templates/eslint.config.js` | ESLint 9 flat config baseline |
| `templates/package.json.snippet.json` | package.json scripts + engines snippet |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-javascript-modern.py` | Validate config bundle against schema | After bundle draft, before landing PR |

## Related

- - [[code-quality-trends]] — quarterly refresh of these rules.
- - [[javascript-testing]] — test config sits on top of this bundle.

## Decision tree

See `content/06-decision-tree.xml`. Branches on runtime (Node 22 / Bun / browser / edge) → tsconfig target + lib. Then on monorepo? → pnpm workspaces or single package. Then on legacy presence → migration mode.
