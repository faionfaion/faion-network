---
slug: browser-automation
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Designs a resilient Playwright (or Puppeteer) automation with explicit waits keyed on assertions, Page Object Model isolation, anti-flake retry policy, and a kill-switch on selector-churn.
content_id: "84aa85697fc5ebdd"
complexity: medium
produces: code
est_tokens: 4200
tags: [browser, automation, playwright, puppeteer, e2e, page-object]
---
# Browser Automation

## Summary

**One-sentence:** Designs a resilient Playwright (or Puppeteer) automation with explicit waits keyed on assertions, Page Object Model isolation, anti-flake retry policy, and a kill-switch on selector-churn.

**One-paragraph:** Browser automation breaks for three reasons: timing assumptions, brittle selectors, and mixed concerns in page logic. This methodology emits an automation-spec: assertion-based explicit waits (no sleep), Page Object Model per screen, selector-strategy policy (data-test-id &gt; role &gt; text &gt; CSS), a flake budget that fails CI if breached, and an extract-data primitive separated from interaction. Output: automation-spec + page-object scaffold + extract primitive + flake budget.

**Ефективно для:**

- Solo dev whose e2e suite went from green to 60% flaky in a quarter.
- Adding scraping + extraction for a product that needs offline data sync.
- Wiring data-test-id everywhere so the design team can refactor without breaking tests.
- Setting a flake budget that gates merges instead of letting flakes accumulate.

## Applies If (ALL must hold)

- Browser automation runs in CI (not just locally).
- Target site has DOM stability OR data-test-id can be added.
- Author has authority to fail the suite on flake budget breach.

## Skip If (ANY kills it)

- API-only testing (use api-contract-first).
- Visual regression only (use a screenshot-diff methodology).
- Unit-tested code that doesn't need browser.
- Third-party site where data-test-id is impossible AND the surface churns weekly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target URL or app | URL | running app or third party |
| Playwright / Puppeteer | npm dependency | package.json |
| CI runner | GitHub Actions / GitLab CI | platform |
| Flake budget | rate (% per 100 runs) | team-agreed default ≤2% |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[flaky-test-elimination]] | Same anti-flake discipline applies. |
| [[deterministic-test-data-pattern]] | Data fixtures used by automation must be deterministic. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `browser_automation_draft` | sonnet | Bounded synthesis. |
| `browser_automation_validate` | haiku | Mechanical schema check. |
| `browser_automation_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/page-object.js` | Generic Page Object base class with data-test-id helpers |
| `templates/extract.js` | Extraction primitive separated from interaction |
| `templates/output-schema.json` | JSON Schema (draft-07) for the browser-automation artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in browser-automation artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-browser-automation.py` | Validate browser-automation artefact against schema | Pre-commit; CI on each artefact change |

## Related



## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
