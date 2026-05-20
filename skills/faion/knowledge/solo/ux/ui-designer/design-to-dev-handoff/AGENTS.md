---
slug: design-to-dev-handoff
tier: solo
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Canonical design-to-dev handoff bundle and acceptance checklist that survives AI-generated Figma frames: tokens, states, motion, accessibility, and content rules end-to-end.
content_id: "7fbaefda764389d0"
tags: [ux, ui, figma, handoff, tokens, states, motion, accessibility]
---

# Design-to-Dev Handoff

## Summary

**One-sentence:** A handoff bundle spec that pairs every Figma frame with explicit token references, full state coverage, motion specs, content rules, and an acceptance checklist the dev runs before merging.

**One-paragraph:** Solves the recurring failure where AI-generated or rushed Figma frames pass to dev as "pretty pictures" and lose tokens, states, motion, and accessibility along the way. Mechanism: package every screen with (1) referenced tokens from the design system, (2) every interactive state (default / hover / focus / active / disabled / loading / error / empty), (3) motion specs (duration / easing / triggers), (4) content rules (max length, truncation, i18n notes), (5) breakpoint behavior, and (6) accessibility specs (focus order, ARIA, contrast). Primary output: a versioned handoff package + a dev-side acceptance checklist that gates the PR merge.

## Applies If (ALL must hold)

- product has a design system OR design tokens in any form (Figma Variables, Style Dictionary, CSS vars)
- handoff target is a development team / developer that will implement the UI
- screen has interactive elements (forms, buttons, navigation) — pure static landing pages get a lighter version
- feature scope >= 1 screen (single-component handoffs use a shorter component spec instead)

## Skip If (ANY kills it)

- design and dev are the same person — internal walkthrough is faster than formal handoff
- prototype-only / throwaway exploration — formal handoff is wasted on disposable work
- no design system exists yet — establish tokens first (`solo/ux/ui-designer/design-tokens-foundation`)
- single icon swap or copy-only change — write a one-line ticket, not a handoff

## Prerequisites

- design system tokens exist and are referenced (not raw hex / px values) in the Figma file
- Figma file has component variants for at least the primary interactive elements
- copy is finalized OR explicitly marked as placeholder (no Lorem ipsum in handoff)
- screen scope is final — handoff does not start mid-design

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-tokens-foundation` | Handoff must reference tokens from this canonical token model |
| `solo/ux/ui-designer/component-states-coverage` | Per-state inventory rules consumed by this methodology |
| `solo/ux/accessibility-specialist/wcag-baseline-aa` | Accessibility checklist items source from this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: tokens-not-values, every-state-rendered, motion-specs-required, content-rules-explicit, focus-order-documented | ~1000 |
| `content/02-output-contract.xml` | essential | Handoff bundle schema + acceptance checklist contract + forbidden patterns (Lorem ipsum, raw hex, missing states) | ~700 |
| `content/03-failure-modes.xml` | essential | 7 LLM/AI-Figma failure modes (state-collapse, token-drift, motion-vibe, etc.) with detector + repair | ~1200 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `token_reference_audit` | haiku | Walk Figma exports, flag raw values where tokens should be used |
| `state_inventory_check` | sonnet | Compare interactive elements vs required state list per element type |
| `motion_spec_extraction` | sonnet | Pull transition / animation specs and verify duration + easing are explicit |
| `accessibility_audit_cross_screen` | opus | Focus-order, contrast, ARIA across the full flow — needs multi-frame synthesis |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff-package.md` | Per-screen handoff bundle template (frame links, tokens, states, motion, a11y) |
| `templates/dev-acceptance-checklist.md` | Dev-side checklist items (token usage, state parity, motion, a11y) |
| `templates/state-matrix.csv` | Element-by-state matrix (rows: elements, cols: states) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-handoff-bundle.py` | Parses handoff package, flags missing fields against contract | Before sending package to dev |
| `scripts/figma-token-audit.py` | Calls Figma API, lists nodes using raw values instead of tokens | At any time during design; before handoff is mandatory |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer methodologies: `design-tokens-foundation`, `component-states-coverage`, `motion-spec-system`
- external: [Figma Dev Mode](https://www.figma.com/dev-mode/) · [Design Tokens W3C](https://www.w3.org/community/design-tokens/) · [Material Motion Guidelines](https://m3.material.io/styles/motion/overview)
