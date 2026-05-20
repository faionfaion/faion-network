---
slug: edge-case-checklist
tier: solo
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Enumerated edge-case checklist (empty, long-content, slow-network, offline, error, permission-denied, etc.) applied at design handoff to catch state gaps before dev.
content_id: "95a567b5ca18f071"
tags: [ux, edge-cases, empty-state, error-state, offline, ac, handoff, content]
---

# Edge Case Checklist

## Summary

**One-sentence:** A 12-item edge-case checklist (empty, long-content, very-short content, slow-network, offline, partial-load, error, permission-denied, low-perms, rate-limited, dark-mode, RTL) applied to every screen at design handoff to catch states that AI-Figma and human designers systematically forget.

**One-paragraph:** Empty / long-content / slow-network / offline / error states are the most commonly forgotten parts of a UI specification — both human designers and AI-Figma defaults render only the "happy path with realistic content". Mechanism: a 12-item checklist that is APPLIED PER SCREEN at handoff time and at AC-writing time, with each item resolved to one of: state-rendered (with link to the rendered state), explicit N/A (with reason), or copy-only spec (when no separate render needed but content rules apply). Primary output: a per-screen edge-case-resolution record that ships with the design handoff and is referenced by ACs.

## Applies If (ALL must hold)

- screen has dynamic content (lists, forms, async data fetching, user input)
- screen ships to real users (not internal prototype)
- design handoff or AC writing is in progress
- design system has at least basic state coverage (loading, error) — gaps surface where to enrich the system

## Skip If (ANY kills it)

- purely static marketing landing page with no dynamic content
- pre-prototype experiment that won't ship
- screen explicitly scoped to happy-path-only with deferred edge-case work (must be documented)
- screen reuses a fully-coordinated existing component for which edge cases are already covered

## Prerequisites

- design handoff bundle is in progress OR acceptance criteria are being written
- list of content data sources for the screen (so we know what "empty" / "long" / "missing" mean here)
- the team knows which of the 12 edge cases are in-scope for this product (e.g., RTL only if the product supports Arabic / Hebrew)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-to-dev-handoff` | Edge-case resolutions are part of the handoff bundle; consume the bundle spec |
| `solo/product/product-planning/ac-quality-rubric` | Edge-case coverage is one of the 7 AC-quality dimensions; consume that rubric |
| `pro/ux/accessibility-specialist/wcag-baseline-aa` | Some edge cases (e.g., error states) have a11y requirements consumed from this |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 12-item enumeration, resolution-per-item, copy-rules-explicit, in-scope-list-up-front, evidence-link-required | ~1000 |
| `content/02-output-contract.xml` | essential | Per-screen resolution-record schema + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (happy-path-only, N/A-everything, content-not-truncated, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `in_scope_filter` | haiku | Apply product config to filter 12-item list to in-scope subset |
| `per_item_check` | sonnet | For each in-scope item, propose state-or-NA-or-copy-rule |
| `copy_rules_drafting` | sonnet | Generate concrete copy rules (max length, truncation, i18n) per item |
| `cross_screen_consistency` | opus | Audit similar screens for consistent edge-case treatment |

## Templates

| File | Purpose |
|------|---------|
| `templates/edge-case-checklist.md` | Per-screen 12-item checklist printable |
| `templates/resolution-record.json` | JSON Schema for the per-screen output |
| `templates/copy-rules.md` | Truncation / empty-state copy library template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/audit-screen-resolutions.py` | Validates resolution record vs schema; flags N/A entries without reasons | At handoff time |
| `scripts/cross-screen-consistency-audit.py` | Compares similar screens for divergent edge-case treatment | Monthly design review |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer methodologies: `design-to-dev-handoff`, `design-review-pr-checklist`, `component-states-coverage`
- external: [Material — Empty States](https://m3.material.io/components/empty-states/overview) · [NN/g — Error Messages](https://www.nngroup.com/articles/error-message-guidelines/) · [Designing for Real-World Browsers (Smashing Mag)](https://www.smashingmagazine.com/)
