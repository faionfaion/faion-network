---
slug: flaky-test-elimination
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "5e519be4ecfdc44a"
summary: "Eliminate flaky tests by root-cause class (shared state, ordering, timing, network, locator fragility, infra) with one fix-pattern per class, a budgeted quarantine policy, and an explicit close-the-loop rule so the long tail of intermittents cannot rot."
tags: [dev, solo, qa, flaky-tests, quarantine, root-cause]
---
# Flaky Test Elimination

## Summary

Faion's free-tier SKILL.md surfaces "fix flaky tests" as a discovery option but ships no methodology behind it, while flake elimination is the #1 day-to-day QA pain on every team that has CI. This methodology installs a six-class taxonomy for flake root causes (shared state, ordering dependence, timing/race, network non-determinism, locator fragility, infra/runner instability), prescribes one canonical fix pattern per class, and pairs that with a quarantine-with-budget policy: any test can be quarantined, but quarantine capacity is capped (e.g. 1% of suite), has an expiry, and an owner. The long tail cannot rot because expired quarantines fail the build.

## Applies If

- A test suite exists with at least one observed intermittent failure in the last two weeks.
- CI history is queryable for at least 30 days (re-run rates, pass-on-retry counts).
- The team has authority to edit tests, fixtures, and CI configuration.
- A code-side quarantine mechanism is available or can be added (e.g. pytest marker, JUnit tag, Cypress retries config).

## Skip If

- No CI exists yet — establish CI first; flake taxonomy is meaningless without retry data.
- The suite is brand-new (&lt; 100 tests, &lt; 1 month old) — too little signal to classify; fix issues case-by-case.
- The suite is being retired — quarantine the lot, do not invest in classification.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Six testable rules: detection, six-class taxonomy with per-class fix patterns, quarantine budget, expiry, and the close-the-loop rule |

## Related

- parent skill: `solo/dev/`
- triggering activity: `Modernize a 2018-era QA suite into AI-augmented test ops`, `Unflake and parallelize a slow E2E suite`
- neighbouring: `solo/dev/qa-flaky-test-root-cause-taxonomy`, `solo/dev/qa-flake-ledger-template`, `pro/dev/e2e-suite-parallelization`
