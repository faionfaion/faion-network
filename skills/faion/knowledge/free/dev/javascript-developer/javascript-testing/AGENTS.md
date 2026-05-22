---
slug: javascript-testing
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Configures JS/React tests with Vitest (preferred) or Jest + Testing Library + MSW for API mocking + Vitest coverage gates.
content_id: "ced183081762eab2"
complexity: medium
produces: config
est_tokens: 3700
tags: [testing, vitest, jest, testing-library, msw]
---
# JavaScript Testing

## Summary

**One-sentence:** Picks Vitest (default) or Jest, wires Testing Library + MSW, configures branch coverage thresholds, and emits a tested config bundle.

**One-paragraph:** Testing JS/TS today means choosing between Vitest (newer, faster, ESM-native) and Jest (legacy but huge ecosystem). This methodology defaults to Vitest unless the project pins to a Jest-only tool, wires Testing Library for DOM, MSW for HTTP mocking, and configures Vitest's V8 coverage with diff-gates. Output is a config bundle: vitest.config.ts (or jest.config.js), test setup file, MSW server file, and CI snippet. Tied back to `code-coverage` for the gate.

**Ефективно для:**

- Net-new React / Node projects: Vitest з-коробки замість 2-год Jest setup.
- Migration Jest → Vitest: API-compatible, тест-файли часто запускаються as-is.
- MSW integration: per-test handler overrides замість ad-hoc fetch stubs.
- Coverage gates: Vitest's --coverage built-in, без додаткових тулів.

## Applies If (ALL must hold)

- JS or TS project with test surface (UI / API / pure logic).
- Test infrastructure is missing or stale (no test runner OR pinned to Jest 27).
- Owner can run a one-shot migration.

## Skip If (ANY kills it)

- Project uses Bun (use bun:test, see bun-runtime-simple).
- E2E / browser automation is the test surface (Playwright, different methodology).
- Tests are framework-pinned (Angular Karma, etc).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| package.json | JSON | repo root |
| Existing test config | files | repo root |
| UI / API mix | ratio | owner / file inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: vitest-default, testing-library-for-dom, msw-for-http, branch-coverage, no-snapshot-only | 1000 |
| `content/02-output-contract.xml` | essential | Schema for test config bundle | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: snapshot-bloat, fetch-jest-spy, jest-on-vite-project | 700 |
| `content/04-procedure.xml` | essential | 5-step setup procedure | 700 |
| `content/06-decision-tree.xml` | essential | Stack + UI/API tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | Lockfile + framework detection. |
| `draft_config` | sonnet | Per-stack customisation. |
| `draft_msw_handlers` | sonnet | Per-endpoint handler stubs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vitest.config.ts` | Vitest config with coverage |
| `templates/test-setup.ts` | Testing Library + MSW setup |
| `templates/msw-server.ts` | MSW server skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-javascript-testing.py` | Validate test config bundle | After draft, before commit |

## Related

- [[code-coverage]] — same gating layer; this methodology wires the JS half.
- [[javascript-modern]] — TS strict + ESM live underneath this config.

## Decision tree

See `content/06-decision-tree.xml`. Branches: build tool (Vite / Webpack) → Vitest default if Vite. UI surface? → Testing Library. HTTP surface? → MSW. Coverage gate? → branch + diff thresholds.
