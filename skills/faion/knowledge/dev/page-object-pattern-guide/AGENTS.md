# Page Object Pattern at Scale (Playwright / Cypress)

## Summary

**One-sentence:** Page-object discipline for E2E suites: locator hierarchy (role > test-id > css), one method per user action, no implicit waits, per-page contract test guarding against selector drift.

**One-paragraph:** Page-object suites rot from selector drift, implicit waits, and god-class page files. This methodology pins a discipline: every page object exposes one method per user action (not per locator); locators follow the hierarchy role > test-id > css; implicit waits are banned in favour of explicit auto-wait assertions; a per-page contract test pins the public API of each page object so accidental rename breaks at compile time. Output: a spec document + page-object skeleton repo enforced by a `validate-page-object-pattern-guide.py` lint pass.

**Ефективно для:**

- E2E suite churn after every small UI change - lock to role + test-id selectors.
- Page object grows to 800 lines - split when user-actions > 20.
- Flaky tests blamed on 'timing' - replace sleep with explicit waits.
- Selectors duplicated across tests - move into page object.
- Page object public API drifts - install per-page contract test.

## Applies If (ALL must hold)

- team runs E2E suite via Playwright, Cypress, or similar
- suite has >=10 tests covering >=3 user flows
- selectors are currently embedded directly in test files (or partial page objects exist)
- team has authority to refactor test layer

## Skip If (ANY kills it)

- <10 E2E tests - investment not yet warranted
- team uses BDD scenario layer that already abstracts locators
- suite is being deleted and replaced

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| E2E framework | Playwright / Cypress installed + CI-wired | engineering |
| Locator audit | list of selectors used across tests | engineering |
| User-flow map | named flows (login, checkout, search) | product / engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-ac-to-assertion-mapping]] | per-AC assertions feed into page-object actions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / gate) | ~900 |
| `content/05-examples.xml` | essential | End-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-locators` | haiku | Mechanical grep over test files. |
| `design-page-api` | sonnet | Per-flow judgement on action granularity. |
| `draft-contract-tests` | sonnet | Per-page public-API contract authoring. |
| `review-architecture` | opus | Cross-flow synthesis when splitting god-class pages. |

## Templates

| File | Purpose |
|------|---------|
| `templates/page-object-pattern-guide.md` | Markdown skeleton for the Page Object Pattern at Scale (Playwright / Cypress) artefact. |
| `templates/_smoke-test.json` | Minimum viable page-object-pattern-guide record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-page-object-pattern-guide.py` | Validate Page Object Pattern at Scale (Playwright / Cypress) artefact against content/02-output-contract.xml. | After draft, before merge; pre-commit hook. |

## Related

- [[qa-ac-to-assertion-mapping]]
- [[qa-exploratory-charter-template]]
- [[qa-test-pyramid-vs-trophy-decision]]

## Decision tree

See `content/06-decision-tree.xml`. The tree filters on suite size, locator-debt level, and refactor ownership; routes under-scaled suites or xpath-heavy suites away first.
