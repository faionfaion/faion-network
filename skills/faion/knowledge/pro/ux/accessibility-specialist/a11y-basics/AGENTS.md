# Accessibility Basics

## Summary

The entry-level accessibility layer for web products: WCAG POUR principles, A/AA/AAA conformance levels, four evaluation types (automated, manual, assistive-tech, user testing), a five-minute quick-check protocol, and pre-commit gate criteria. Automated scanners catch only ~30% of issues; manual + assistive-tech testing is required for the rest. Use semantic HTML first; reach for ARIA only when no semantic equivalent exists.

## Why

Products without accessibility baseline exclude users with disabilities, create legal compliance risk (ADA, Section 508, AODA), and accumulate expensive late-stage fixes. Wiring axe-core into CI catches regressions at PR time, where fixing a failing input label costs minutes rather than hours in a QA cycle. The POUR framework gives teams a shared vocabulary for categorizing and prioritizing issues.

## When To Use

- Onboarding a team or codebase to accessibility for the first time.
- Pre-launch sanity sweep on a small site or feature where a full WCAG 2.2 conformance audit is overkill.
- Wiring CI to catch the obvious 30% automated tools find: missing alt, unlabelled inputs, contrast failures, heading skips.
- Educating a new agent or developer before they edit UI code.

## When NOT To Use

- Final compliance sign-off — use `wcag-22-compliance` and `regulatory-compliance-2026`.
- Real assistive-technology testing flows (NVDA/VoiceOver/TalkBack) — use `testing-with-assistive-technology`.
- Procurement / VPAT-ACR generation — use `regulatory-compliance-2026`.
- XR/spatial experiences — use `vr-design-patterns`, `ar-design-patterns`, `spatial-accessibility`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-wcag-principles.xml` | POUR principles, A/AA/AAA levels, four evaluation types, five-minute test protocol |
| `content/02-common-issues.xml` | Form labels, image alt text, contrast, keyboard access; code examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y-ci.js` | Playwright + axe-core CI gate for WCAG 2.2 AA across defined routes |
