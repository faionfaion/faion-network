# Testing with Assistive Technology

## Summary

A three-tier AT testing strategy: automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), user-with-disability session (quarterly). Automated tools catch only 30–50% of real issues; screen-reader audio, switch-control, and lived-experience testing cannot be replaced by any automated tool. Each bug report must include: WCAG SC reference, repro snippet, suggested ARIA APG pattern, and scope estimate.

## Why

WCAG 2.2 AA conformance claims based on automated scan results alone are legally and technically invalid. The gap (50–70% of real issues missed) is dominated by dynamic-content failures, focus-order errors, and ARIA misuse on custom components — exactly what screen-reader users encounter daily. Filing AT bugs without WCAG citations and repros causes them to be postponed indefinitely.

## When To Use

- Pre-release accessibility QA for any public web/app.
- Validating WCAG 2.2 AA / EN 301 549 / ADA Title II conformance claims.
- Regression-testing custom components (combobox, modal, tree, datagrid).
- Investigating user complaints from screen-reader or keyboard-only users.
- Audit work for legal-risk reduction on B2C and government products.

## When NOT To Use

- Pure backend/API services with no UI surface.
- Internal tools where the user population is confirmed non-AT (still test keyboard).
- Early-stage paper prototypes — methodology requires an interactive build.
- As a substitute for design-time accessibility — testing alone won't fix architectural debt.

## Content

| File | What's inside |
|------|---------------|
| `content/01-testing-layers.xml` | Three-tier strategy, SR/browser matrix, keyboard test keys, common failure taxonomy. |
| `content/02-rules-and-antipatterns.xml` | Bug-report rules, agentic workflow, gotchas (ARIA invention, false-pass patterns). |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y-gate.sh` | CI script: fail PR if axe-core finds serious/critical WCAG 2.2 AA violations. |
