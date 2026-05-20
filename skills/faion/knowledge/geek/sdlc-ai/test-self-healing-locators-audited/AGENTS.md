---
slug: test-self-healing-locators-audited
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.
content_id: "8e2c9b1996e83fc5"
tags: [self-healing, playwright, e2e-testing, locators, accessibility-tree]
---
# Self-Healing Locators with Mandatory Audit Diff

## Summary

**One-sentence:** In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.

**One-paragraph:** In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.diff` or equivalent) before the next CI run consumes it. Auto-healing without an audit trail is silent test rot; allowing arbitrary CSS-substitution heals is how an E2E suite ends up clicking the wrong button on a payment screen.

## Applies If (ALL must hold)

- Large E2E suites (>200 tests) with regular UI churn from a fast-shipping product team.
- Design-system migrations and component-rename refactors where DOM changes en masse.
- Cypress / Playwright projects already using role-based or test-id locators (`getByRole`, `getByTestId`).
- Cross-browser regression suites where flake from selector drift dominates failures.

## Skip If (ANY kills it)

- High-stakes flows: payments, login, role-elevation, account deletion — wrong heal = wrong click = silent prod regression.
- Small E2E suites (<50 tests) where humans can repair selectors faster than reviewing heal diffs.
- Suites that locate elements by visual position or pixel coordinate — no accessible name to anchor on.
- A/B-tested UI where the same role+name appears in two variants — heals collide.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
