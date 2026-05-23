---
slug: handoff-spec-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single Markdown artefact that closes design→engineering handoff loss: states, tokens, motion, accessibility, edge cases, and code map are all named in one file with token references and pixel-accurate measurements.
content_id: "83547f89fb57b2a6"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["handoff", "design-to-dev", "spec", "states", "accessibility"]
---
# Handoff Spec Template

## Summary

**One-sentence:** Single Markdown artefact that closes design→engineering handoff loss: states, tokens, motion, accessibility, edge cases, and code map are all named in one file with token references and pixel-accurate measurements.

**One-paragraph:** Most design→engineering handoff loss comes from missing states, undocumented motion, and ambiguous accessibility. This template pins a six-section spec: every component carries an explicit list of states (default/hover/active/focus/disabled/loading/error/empty), token references (no raw hex), motion specs (duration + easing), accessibility annotations (focus order, labels, contrast), edge cases (long text, RTL, slow network), and a code map that names the file + component to extend.

**Ефективно для:**

- Solo founder doing design + eng work who needs a single artefact to remember every state.
- Designer + remote engineer handoff where Loom-only handoffs miss states.
- AI agent generating React/Vue components that need explicit state coverage to avoid hallucinated defaults.
- Pre-launch QA where missing-state bugs surface in production.

## Applies If (ALL must hold)

- A component or screen design is ready for engineering and has at least 2 interactive states.
- Design tokens (or a token-equivalent palette) are already defined.
- Code repository structure is known so the code map can name files.
- Engineering owner (or AI agent) is ready to consume the spec.

## Skip If (ANY kills it)

- Static marketing image with no interactive states.
- Throwaway prototype with no production users.
- Design system primitive that lives in Storybook with its own spec — extend the Storybook entry instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma frame or screen | Figma URL | Design canvas |
| Design tokens reference | JSON or Figma variables | Design system repo |
| Code map: file + component | string | Frontend repo |
| Accessibility audit baseline | WCAG checklist | a11y review tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-to-dev-handoff` | Process layer this spec sits inside. |
| `solo/ux/ui-designer/design-tokens-fundamentals` | Token references used by this spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-states-and-motion` | sonnet | Per-component judgement on state coverage and motion params. |
| `validate-tokens-and-a11y` | haiku | Deterministic token reference check + WCAG threshold check. |
| `cross-component-audit` | opus | Multi-spec audit for consistency across a screen flow. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff-spec-template.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/handoff-spec-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-handoff-spec-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-to-dev-handoff]]
- [[edge-case-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
