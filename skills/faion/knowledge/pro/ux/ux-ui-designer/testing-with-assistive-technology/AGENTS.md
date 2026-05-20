---
slug: testing-with-assistive-technology
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-tier AT testing strategy: automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), user-with-disability session (quarterly).
content_id: "ce2fa9cf82831858"
tags: [accessibility, wcag, testing, assistive-technology, screen-reader]
---
# Testing with Assistive Technology

## Summary

**One-sentence:** A three-tier AT testing strategy: automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), user-with-disability session (quarterly).

**One-paragraph:** A three-tier AT testing strategy: automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), user-with-disability session (quarterly). Automated tools catch only 30–50% of real issues; screen-reader audio, switch-control, and lived-experience testing cannot be replaced by any automated tool. Each bug report must include: WCAG SC reference, repro snippet, suggested ARIA APG pattern, and scope estimate.

## Applies If (ALL must hold)

- Pre-release accessibility QA for any public web/app.
- Validating WCAG 2.2 AA / EN 301 549 / ADA Title II conformance claims.
- Regression-testing custom components (combobox, modal, tree, datagrid).
- Investigating user complaints from screen-reader or keyboard-only users.
- Audit work for legal-risk reduction on B2C and government products.

## Skip If (ANY kills it)

- Pure backend/API services with no UI surface.
- Internal tools where the user population is confirmed non-AT (still test keyboard).
- Early-stage paper prototypes — methodology requires an interactive build.
- As a substitute for design-time accessibility — testing alone won't fix architectural debt.

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

- parent skill: `pro/ux/ux-ui-designer/`
