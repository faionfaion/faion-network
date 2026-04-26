# Testing with Assistive Technology

## Summary

Manual testing with real screen readers, keyboard-only navigation, and mobile AT to catch the 50-70% of accessibility issues that automated tools miss. Covers NVDA, JAWS, VoiceOver (macOS/iOS), and TalkBack (Android), with tiered test workflows from 15-minute smoke checks to 4-hour comprehensive audits.

## Why

Automated scanners (axe, WAVE, Lighthouse) detect ~30-50% of WCAG violations. The remainder — focus management bugs, incorrect live-region timing, custom-widget semantics, and misleading alt text — only surface when a real AT processes the DOM and produces speech output. AT + browser pairings matter and diverge; passing one combo does not generalize.

## When To Use

- Verifying screen-reader and keyboard parity before any web, iOS, Android, or Electron release.
- Catching focus-management regressions (modal close, route transitions, toast announcements).
- Reproducing user-reported AT bugs with the exact screen reader + browser combo they use.
- Authoring Gherkin test cases that a Guidepup agent or human tester can execute.
- Pre-release sign-off on custom widgets (combobox, tree, grid, live regions).

## When NOT To Use

- First-pass scanning — run `a11y-testing` with axe/Pa11y first to remove easy issues.
- Compliance paperwork / VPAT generation — use `regulatory-compliance-2026` with AT findings as input.
- Native mobile UI design reviews (not runtime AT) — those are design-phase concerns.
- Fully automated AT-driven E2E without human verification — screen-reader automation reads the accessibility tree, not real speech; results lie.

## Content

| File | What's inside |
|------|---------------|
| `content/01-at-platforms.xml` | Screen reader matrix (NVDA, JAWS, VoiceOver, TalkBack, Orca): key commands, browser pairings, market share. |
| `content/02-keyboard-testing.xml` | Keyboard-only navigation rules: tab order, focus indicators, custom-component interactions, common failures. |
| `content/03-screen-reader-checklist.xml` | Structured checklist: content, structure, forms, navigation, dynamic content, custom components. |
| `content/04-test-workflows.xml` | Tiered workflows: 15-min smoke, 2-4h comprehensive. Agentic pipeline (Playwright + Guidepup + human sign-off). |

## Templates

| File | Purpose |
|------|---------|
| `templates/guidepup-nvda-form-error.js` | Playwright + Guidepup test asserting inline form error announced by NVDA. |
| `templates/at-test-case.txt` | Gherkin template for authoring AT test cases per WCAG SC. |
