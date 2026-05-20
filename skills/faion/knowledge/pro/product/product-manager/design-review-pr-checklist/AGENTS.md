---
slug: design-review-pr-checklist
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: PR-time design-QA checklist (tokens used, components reused, motion respects prefers-reduced-motion, a11y intact, content rules honored) — gates whether the implementation matches the design.
content_id: "971126a8b72c2199"
tags: [product, design-qa, pr-review, design-system, tokens, motion, accessibility]
---

# Design Review PR Checklist

## Summary

**One-sentence:** A PR-time design-QA checklist (10 items across token usage, component reuse, motion compliance, accessibility, content rules, breakpoint coverage) that gates whether the implementation matches the design handoff.

**One-paragraph:** Design handoff (`solo/ux/ui-designer/design-to-dev-handoff`) covers the upstream side; this methodology covers the downstream side: once dev opens the PR, who validates the implementation adheres to the design? The checklist runs at PR time as a required reviewer (typically a designer or design-engineer) verifying that the dev didn't drift from the handoff — token usage, component reuse, motion specs, accessibility, content rules, breakpoint behavior. Primary output: a per-PR design-QA record + a pass / changes-needed decision that blocks merge until design adherence is verified.

## Applies If (ALL must hold)

- product has a design system with tokens + component library
- design-to-dev handoff methodology in use OR similar handoff bundle exists
- PR touches UI code (components, styles, routes) — backend / docs-only PRs skip
- a designer or design-engineer is available as a PR reviewer (or rotates for coverage)

## Skip If (ANY kills it)

- no design system in place — establish tokens + components first
- single-person dev-and-designer team — self-review checklist is sufficient
- prototype / spike PR explicitly marked "experimental, not for design adherence"
- design adherence is acknowledged out-of-scope for the project phase (early MVP); add later

## Prerequisites

- design system documentation accessible (token catalog, component catalog with intended use)
- design handoff package linked from the story / PR (includes specified tokens, states, motion, content rules)
- designer / design-engineer time allocated for PR reviews (cap: ~20% of their week)
- PR-platform supports required-reviewer rules (block merge until design reviewer approves)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-to-dev-handoff` | This methodology validates that the PR matches the handoff bundle from that methodology |
| `solo/dev/testing-developer/a11y-no-regression-pr-gate` | A11y portion of this checklist overlaps; consume that gate's output |
| `solo/dev/software-architect/architect-pr-review-checklist` | Architectural review runs in parallel; this methodology stays in the design lane |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 10-item-checklist, designer-reviewer-required, evidence-per-item, no-style-cleanup-creep, handoff-deltas-flagged-back | ~1000 |
| `content/02-output-contract.xml` | essential | Design-QA record schema + PR-comment contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (rubber-stamp design review, token bypass, motion guess, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pr_diff_classification` | haiku | Identify if PR touches UI files (components / styles / routes) |
| `token_usage_audit` | sonnet | Diff PR vs token catalog; flag raw values |
| `component_reuse_check` | sonnet | Detect duplicated components instead of design-system reuse |
| `motion_a11y_audit` | sonnet | Verify motion, prefers-reduced-motion, focus order in implemented code |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-qa-checklist.md` | 10-item checklist printable card |
| `templates/design-qa-record.json` | JSON Schema for the per-PR record |
| `templates/pr-comment.md` | PR comment template with per-item status |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scan-pr-for-raw-values.py` | Lints PR diff for raw colors / spacing / px instead of token usage | Every UI-touching PR |
| `scripts/audit-component-reuse.py` | Detects new components vs design-system catalog | Every UI-touching PR |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: `design-to-dev-handoff`, `a11y-no-regression-pr-gate`, `design-review-facilitation-script`
- external: [Material Design QA Checklist](https://m3.material.io/foundations/quality-checklist) · [Atlassian Design QA at PR Time](https://atlassian.design/) · [Polaris Component Adoption Metrics](https://polaris.shopify.com/)
