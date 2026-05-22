---
slug: e2e-testing
tier: free
group: dev
domain: dev
version: 2.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: 3cce83eedd49fd30
summary: Produces an E2E test-suite config (Playwright primary, Cypress secondary) with POM, storageState auth, route-mocked APIs, sharded CI, and trace artefacts.
complexity: medium
produces: config
est_tokens: 4400
tags: [e2e, playwright, cypress, testing, browser-automation]
---
# E2E Testing

## Summary

**One-sentence:** Produces an E2E test-suite config (Playwright primary, Cypress secondary) with POM, storageState auth, route-mocked APIs, sharded CI, and trace artefacts.

**One-paragraph:** E2E suites validate full user journeys across real browsers. Without structure (Page Object Model, fixtures, data factories, sharding) they become slow, flaky, and silently disabled. This methodology turns a project's user-journey list into a runnable Playwright project: config file, POM base class, storageState auth, route-mocked third-party APIs, factory functions, and a sharded GitHub Actions workflow with merged blob reports.

**Ефективно для:** team migrating off slow Cypress suites or starting a fresh Playwright project who needs a defensible structure on day one.

## Applies If (ALL must hold)

- Writing or reviewing Playwright / Cypress test suites for a real web app.
- Setting up E2E infrastructure from scratch (config, auth, CI sharding).
- Debugging flaky tests or selector failures.
- Adding visual regression checks (component-scoped, masked).
- Migrating from Cypress to Playwright.

## Skip If (ANY kills it)

- Unit or integration scope (no browser needed) → use unit-testing or testing-pytest.
- API-only testing — use an HTTP client instead.
- OAuth flows with real external providers (use API-token injection workaround, not UI login).
- Single-developer prototype with no production users.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `user-journeys.yaml` | list of {journey_name, steps, expected_outcome} | operator |
| `app-base-url` | URL | infra |
| `test-user-credentials` | 1Password entry | secrets store |
| `ci-machine-count` | integer (shard target) | CI config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-patterns]] | AAA / Given-When-Then framing used inside each test. |
| [[github-repo-bootstrap]] | CI workflow lives in a repo with branch protection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: pyramid, POM, role selectors, storageState, route mocking, factories, no fixed sleeps, sharded CI. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the emitted suite-config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: fixed sleep, CSS selectors, full-page screenshots, UI OAuth, shared test state. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate journeys → scaffold POM → wire auth → shard CI → publish report. | ~700 |
| `content/05-examples.xml` | recommended | Checkout-flow journey worked end to end with POM + factory. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Playwright vs Cypress; full vs component screenshot; sharded vs single-runner. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_journeys` | haiku | Mechanical YAML→typed list. |
| `scaffold_pom` | sonnet | Tradeoffs (which selectors, which fixtures) require sound reasoning. |
| `audit_flakiness_risks` | opus | Subtle cross-test contamination + selector brittleness. |
| `emit_ci_workflow` | sonnet | Mechanical YAML emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/playwright.config.ts` | Full Playwright config: projects, sharding, reporter, retries. |
| `templates/pom-base.ts` | Abstract base Page class with navigation helpers. |
| `templates/auth-setup.ts` | storageState auth setup fixture. |
| `templates/factory.ts` | Data factory with faker, builder pattern. |
| `templates/ci-workflow.yml` | GitHub Actions sharded Playwright workflow. |
| `templates/_smoke-test.yaml` | Minimum journey list (login → dashboard). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-e2e-testing.py` | Validates emitted suite-config JSON against the schema. | Pre-commit; in CI before publishing config. |

## Related

- [[testing-patterns]]
- [[unit-testing]]
- [[mocking-strategies]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches first on `framework` (greenfield → Playwright; legacy Cypress maintained → Cypress with migration plan), then on `visual_regression_needed` (component-scoped vs none), then on `ci_machine_budget` (≥4 → shard; <4 → single runner). Each leaf cites a rule id in 01-core-rules.xml.
