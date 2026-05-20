---
slug: page-object-pattern-guide
tier: solo
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0db747319c0f9a91"
summary: A maintainable page-object pattern for Playwright and Cypress at scale, with a locator-convention discipline (role > test-id > css), one-method-per-user-action API, no implicit waits, and a per-page contract test that prevents selector drift from rotting the suite.
tags: [playwright, cypress, page-object, e2e, locators, maintainability]
---

# Page Object Pattern at Scale (Playwright / Cypress)

## Summary

**One-sentence:** Define a maintainable Page Object pattern for E2E suites — locator convention, one-method-per-user-action API, no implicit waits, per-page contract tests — that keeps the test suite from rotting as the UI evolves.

**One-paragraph:** Playwright and Cypress methodologies teach automation basics but not the structural pattern that prevents 50-page test suites from becoming unmaintainable after 6 months. The failure mode is universal: every page object accumulates ad-hoc helper methods, CSS selectors drift apart, implicit waits hide flakiness, and a single UI rename breaks 30 tests because every test reaches into the DOM directly. This methodology pins the four discipline points: (1) a locator convention with a single priority order (role > test-id > css, never mix), (2) one method per user-meaningful action ("login as user", not "type username", "type password", "click submit"), (3) explicit waits and assertions only (no `page.waitForTimeout`, no `cy.wait(2000)`), (4) a per-page contract test that runs the page object's public surface against a known-good snapshot so selector drift fails CI in the page-object PR, not in 30 downstream test PRs. Primary output: a `pages/` directory structure, a base PageObject class, and a contract-test runner.

## Applies If (ALL must hold)

- team uses Playwright OR Cypress at scale (≥ 20 E2E tests OR ≥ 5 pages under test)
- E2E suite has shown flakiness or unmaintainability symptoms (broken-test backlog &gt; 5 tests OR test rewrites every UI rename)
- team has at least one engineer dedicated to keeping E2E green
- E2E suite is run on a CI pipeline that blocks merges (not informational only)

## Skip If (ANY kills it)

- E2E suite is fewer than 10 tests — direct-DOM access is cheaper than the page-object overhead
- team has zero capacity for refactor — adopting the pattern requires a one-time refactor that takes 1-3 days of dedicated work
- product is mostly API-based with thin UI — invest in contract tests instead (`geek/sdlc-ai/test-consumer-contract-from-spec`)
- already on a working page-object pattern that the team is happy with — do not refactor on principle alone

## Prerequisites

- Playwright or Cypress installed and running at least one E2E test in CI
- typed test language (TypeScript strongly preferred; JavaScript with JSDoc minimally acceptable)
- engineering buy-in for adding `data-testid` (or equivalent) attributes to UI components when role-based locators are not sufficient

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-test-pyramid-vs-trophy-decision` | Decides whether to invest in E2E at all before refining the pattern |
| `geek/sdlc-ai/test-self-healing-locators-audited` | AI-assisted locator audit for the locator convention |
| `solo/dev/testing-developer/qa-exploratory-charter-template` | Sibling discipline that catches what E2E does not |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: locator convention, one-action-one-method, explicit waits only, per-page contract test, no implementation leak | ~900 |
| `content/02-output-contract.xml` | essential | Page-object class schema, public surface contract, contract-test schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: locator mix, implicit waits, fat page objects, test-helper sprawl, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_user_actions_from_test_intentions` | sonnet | Per-test extraction with naming judgment |
| `propose_locator_priority_per_element` | sonnet | Per-element bounded judgment |
| `generate_page_object_skeleton` | haiku | Template fill once user actions are listed |
| `contract_test_diff_review` | sonnet | Bounded review of selector-drift diffs |

## Templates

| File | Purpose |
|------|---------|
| `templates/base-page-object.ts` | Playwright base class with locator-priority helpers and explicit-wait helpers |
| `templates/base-page-object-cypress.ts` | Cypress equivalent with cy.findByRole helpers |
| `templates/contract-test.spec.ts` | Per-page contract test skeleton that validates the public surface |
| `templates/page-object.template.ts` | Single-page-object skeleton with sections wired up |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/locator-audit.py` | Walks `pages/`, flags any locator that mixes role + test-id + css OR uses brittle css (nth-child, attribute selectors on layout classes) | Pre-commit hook |
| `scripts/contract-snapshot.sh` | Runs the per-page contract test and updates snapshots on demand | When the page-object PR introduces a deliberate selector change |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-exploratory-charter-template`, `solo/dev/testing-developer/qa-test-pyramid-vs-trophy-decision`
- external: [Selenium Page Object Pattern (Selenium docs)] · [Playwright Page Object Models (official docs)] · [Cypress Selector Playground best practices] · [Kent C. Dodds Testing JavaScript Course on user-centric locators]
