---
slug: testing-with-assistive-technology
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Manual testing with real screen readers, keyboard-only navigation, and mobile AT to catch the 50-70% of accessibility issues that automated tools miss.
content_id: "ce2fa9cf82831858"
tags: [accessibility, testing, screen-reader, wcag, assistive-technology]
---
# Testing with Assistive Technology

## Summary

**One-sentence:** Manual testing with real screen readers, keyboard-only navigation, and mobile AT to catch the 50-70% of accessibility issues that automated tools miss.

**One-paragraph:** Manual testing with real screen readers, keyboard-only navigation, and mobile AT to catch the 50-70% of accessibility issues that automated tools miss. Covers NVDA, JAWS, VoiceOver (macOS/iOS), and TalkBack (Android), with tiered test workflows from 15-minute smoke checks to 4-hour comprehensive audits.

## Applies If (ALL must hold)

- Verifying screen-reader and keyboard parity before any web, iOS, Android, or Electron release.
- Catching focus-management regressions (modal close, route transitions, toast announcements).
- Reproducing user-reported AT bugs with the exact screen reader + browser combo they use.
- Authoring Gherkin test cases that a Guidepup agent or human tester can execute.
- Pre-release sign-off on custom widgets (combobox, tree, grid, live regions).

## Skip If (ANY kills it)

- First-pass scanning — run `a11y-testing` with axe/Pa11y first to remove easy issues.
- Compliance paperwork / VPAT generation — use `regulatory-compliance-2026` with AT findings as input.
- Native mobile UI design reviews (not runtime AT) — those are design-phase concerns.
- Fully automated AT-driven E2E without human verification — screen-reader automation reads the accessibility tree, not real speech; results lie.

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

- parent skill: `pro/ux/accessibility-specialist/`
