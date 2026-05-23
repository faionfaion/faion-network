# Testing in JavaScript / TypeScript

## Summary

**One-sentence:** Produces a Vitest-or-Jest test suite with React Testing Library, MSW v2 API mocks, fake timers, and ESM-aware coverage config — runtime picked from build-tool fingerprint.

**One-paragraph:** Covers the Vitest vs Jest decision tree (2026), unit and component testing patterns, React Testing Library integration, MSW v2 for API mocking, fake timers, coverage configuration, and common pitfalls (ESM/CJS confusion, jsdom layout limitations, MSW v1→v2 migration, fake timer leaks). The JS testing ecosystem fragmented between Jest (CommonJS-native) and Vitest (ESM-native, Vite-integrated); choosing the wrong runner or misconfiguring the environment causes non-deterministic results.

**Ефективно для:** new Vite/Next/Remix/Astro projects (Vitest), existing CRA/legacy Jest projects (Jest), React component tests, Node.js HTTP-client unit tests, hook tests under React 18+, mocking outbound fetch with MSW.

## Applies If (ALL must hold)

- Setting up a new JavaScript/TypeScript test suite (Vitest or Jest)
- Migrating Jest to Vitest or upgrading MSW v1 to v2
- Adding React Testing Library tests for components or hooks
- Mocking outbound HTTP at the network layer instead of stubbing modules
- Configuring coverage thresholds in a Vite or webpack pipeline

## Skip If (ANY kills it)

- Go tests — use `[[testing-go]]`
- Python tests — use `[[testing-pytest]]`
- Cross-browser end-to-end — use `[[e2e-testing]]`

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `package.json` with `type: module` or CommonJS | JSON | project root |
| Build tool fingerprint | vite.config.* OR webpack.config.* OR next.config.* | project root |
| Test framework dep | `vitest` or `jest` in devDependencies | `npm install` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[testing-patterns]]` | AAA, builder, POM patterns reused |
| `[[mocking-strategies]]` | When to mock vs use real collaborator |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick Vitest vs Jest | sonnet | Deterministic from config fingerprint. |
| Author component test | sonnet | Pattern application from template. |
| Debug ESM/CJS interop crash | opus | Cross-cuts bundler, runner, transformer chain. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vitest.config.ts.tmpl` | Vitest config with jsdom env, coverage, setup file path. |
| `templates/jest.config.cjs.tmpl` | Jest config with jsdom env, transform, coverage thresholds. |
| `templates/setup.ts.tmpl` | Test setup: jest-dom + MSW server + timer teardown. |
| `templates/component.test.tsx.tmpl` | React component test using `screen.getByRole` + MSW handler. |
| `templates/_smoke-test.test.ts` | Minimal Vitest sanity test verifying the toolchain. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-javascript.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/dev/testing-developer/`
- `[[testing-go]]`
- `[[testing-pytest]]`
- `[[testing-patterns]]`
- `[[unit-testing]]`
- `[[mocking-strategies]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether testing-javascript applies: root question — "Does the project ship via Vite, Next, Remix, or Astro?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
