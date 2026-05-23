---
slug: a11y-no-regression-pr-gate
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "CI / PR gate that blocks merges on NEW accessibility violations vs a VCS-tracked baseline, with explicit time-boxed waivers and severity-stratified blocking."
content_id: "0f742257a0b03734"
complexity: medium
produces: config
est_tokens: 5300
tags: [a11y, accessibility, ci, pr-gate, wcax, axe, regression-budget]
---
# A11y No-Regression PR Gate

## Summary

**One-sentence:** CI / PR gate that blocks merges on NEW accessibility violations vs a VCS-tracked baseline, with explicit time-boxed waivers and severity-stratified blocking.

**One-paragraph:** Zero-violation a11y gates create ceremony everyone routes around; this methodology installs a net-regression gate. Only NEW violations vs `.a11y/baseline.json` (committed to VCS) block PRs; waivers live in `.a11y-waivers.json` with WCAG ID + route + selector + rationale + reviewer + 90-day expiry; the gate scans only routes / stories impacted by the diff; severity-stratified blocking auto-blocks new critical/serious and requires PR-description ack for moderate/minor. Output: a versioned `.a11y/gate-config.json` consumed by the CI workflow.

**Ефективно для:**

- Zero-violation gate is being routed around - install net-regression ratchet.
- Waivers never expire - 90-day cap forces re-evaluation.
- Baseline edited from feature branches - lock to main-only via PR review.
- Full-site scan slows every PR - scope to diff-impacted routes.
- All violations block equally - stratify by axe severity.

## Applies If (ALL must hold)

- team uses a CI system that can block PRs
- a11y scanning tool is available (axe-core, pa11y, Lighthouse CI)
- PRs are review-merged (not auto-merged) so waivers + acks are visible
- team owns the codebase and can commit baseline + waiver files

## Skip If (ANY kills it)

- team has no review gate (auto-merge on green)
- no a11y scanner can be wired (no DOM surface)
- regulated industry mandates zero-violation gate - use that instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| a11y scanner | axe-core / pa11y / Lighthouse CI in CI | engineering |
| Route map | .a11y/route-map.json or framework convention | frontend |
| Baseline file | .a11y/baseline.json committed to main | engineering |
| Waiver file | .a11y-waivers.json (may start empty) | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-changed-lines-coverage-dashboard]] | diff-only metrics share the route-map; coordinate paths |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / gate) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diff-route-mapping` | haiku | Mechanical file -> route lookup. |
| `severity-stratified-decision` | sonnet | Per-violation judgement on block vs ack. |
| `waiver-review` | opus | Cross-input synthesis when waiving live a11y issues. |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y-no-regression-pr-gate.md` | Markdown skeleton for the A11y No-Regression PR Gate artefact. |
| `templates/_smoke-test.json` | Minimum viable a11y-no-regression-pr-gate record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-no-regression-pr-gate.py` | Validate A11y No-Regression PR Gate artefact against content/02-output-contract.xml. | After draft, before merge; pre-commit hook. |

## Related

- [[qa-changed-lines-coverage-dashboard]]
- [[qa-risk-matrix-method]]
- [[security-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree filters on scanner presence, VCS-baseline discipline, and per-PR new-violation severity; routes critical/serious new violations to block and moderate/minor to ack-required.
