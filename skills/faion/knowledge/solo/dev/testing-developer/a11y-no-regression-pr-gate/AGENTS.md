---
slug: a11y-no-regression-pr-gate
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: CI / PR gate that blocks merges on new accessibility regressions against a baseline budget, with an explicit waiver workflow for documented exceptions.
content_id: "b62ce01261b793a5"
tags: [a11y, accessibility, ci, pr-gate, wcag, axe, pa11y, regression-budget]
---

# A11y No-Regression PR Gate

## Summary

**One-sentence:** A CI gate that runs axe-core / pa11y against the changed routes on every PR, compares to a stored baseline, blocks merge on new violations, and provides a waiver workflow for documented exceptions.

**One-paragraph:** Solves the gap where general a11y testing methodology exists but the operational CI / PR gate + waiver workflow do not. Mechanism: on every PR (a) detect changed routes / components from the diff, (b) run axe-core (or pa11y) headless against those routes, (c) compare violation set to a baseline JSON stored in the repo, (d) block merge if NEW violations appear, (e) allow merge if violations are unchanged or reduced, (f) provide a `.a11y-waivers.json` file where waived violations are listed with rationale, expiry, and reviewer sign-off. Primary output: a PR check that is green when net accessibility has not regressed and red with a diff when it has.

## Applies If (ALL must hold)

- product has a UI (web app, marketing site)
- CI exists with PR-blocking checks (GitHub Actions, GitLab CI, CircleCI, Buildkite)
- repo can host a baseline file under version control
- team has an accessibility-aware lead OR an external auditor for waiver review

## Skip If (ANY kills it)

- pure backend / API repo with no UI
- WCAG conformance not a project goal AND no contractual / regulatory requirement
- product is in pre-launch prototype phase with no users — establish a baseline first; add the gate at launch
- team will treat the gate as ceremony only and waive everything — fix the culture first

## Prerequisites

- one of: axe-core, pa11y, lighthouse-ci installed and runnable against built artifacts (Storybook, dev server, or static export)
- a baseline JSON (`a11y-baseline.json`) committed to repo, generated from the current state of the trunk
- list of routes / Storybook stories the gate scans (avoid scanning every page on every PR — too slow)
- waiver review SLA documented (e.g., "tech lead reviews within 1 business day")

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/accessibility-specialist/wcag-baseline-aa` | Defines the WCAG 2.2 AA rule set the gate enforces |
| `pro/ux/accessibility-specialist/a11y-test-automation` | Source of axe / pa11y test patterns the gate runs |
| `solo/dev/testing-developer/visual-regression-baseline` | Same baseline-and-diff pattern; share infrastructure |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: net-regression-only, baseline-in-vcs, explicit-waivers-only, route-detection-from-diff, severity-stratified-blocking | ~1000 |
| `content/02-output-contract.xml` | essential | Gate output schema + waiver record schema + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (waiver-everything, baseline-drift, flaky-rules, etc.) with detector + repair | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `changed_route_detection` | haiku | Walk PR diff, map files to routes / stories |
| `violation_diff_against_baseline` | sonnet | Compare current scan to baseline; classify new / fixed / unchanged |
| `waiver_proposal_drafting` | sonnet | For unfixable-immediately violations, draft a waiver entry with WCAG criterion + rationale |
| `gate_decision` | haiku | Pass/fail based on diff + waivers; mechanical |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y-baseline.json` | Baseline JSON schema (per-route violation set) |
| `templates/a11y-waivers.json` | Waiver registry schema (criterion, rationale, reviewer, expiry) |
| `templates/gate-output.json` | PR comment / annotation JSON schema |
| `templates/ci-workflow.yml` | Sample GitHub Actions workflow runnable as drop-in |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/a11y-diff.py` | Computes new / fixed / unchanged violations vs baseline | Every PR run |
| `scripts/validate-waivers.py` | Checks `.a11y-waivers.json` against schema, flags expired waivers | Pre-merge and weekly cron |
| `scripts/rebase-baseline.py` | Regenerates baseline after net-fix PRs land | On main branch after a fix-PR merges |

## Related

- parent skill: `solo/dev/testing-developer/`
- peer methodologies: `visual-regression-baseline`, `lighthouse-perf-budget`, `pr-merge-checks-floor`
- external: [axe-core rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md) · [WCAG 2.2 Quick Ref](https://www.w3.org/WAI/WCAG22/quickref/) · [pa11y CI docs](https://github.com/pa11y/pa11y-ci)
