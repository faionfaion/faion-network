---
slug: accessibility-first-design
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for designing UI components with accessibility as a structural constraint, not a post-build patch — keyboard, SR, contrast, motion baked in.
content_id: "46b1c92f70bb59fd"
complexity: medium
produces: spec
est_tokens: 4800
tags: [accessibility-first, design, ux, wcag, ia]
---
# Accessibility-First Design

## Summary

**One-sentence:** Spec for designing UI components with accessibility as a structural constraint, not a post-build patch — keyboard, SR, contrast, motion baked in.

**One-paragraph:** Bolting accessibility onto a finished design produces fragile patches and re-work. Accessibility-first design treats keyboard order, SR semantics, contrast budget, target size, and reduced-motion alternates as constraints during wireframe + spec, not lint-time discoveries. This methodology pins the design-doc checklist (semantic structure, focus order spec, ARIA budget, contrast tokens, motion alternates), the design-review rubric, and the handoff artefact that engineers can implement without re-deriving the accessibility intent.

**Ефективно для:**

- Designers ship specs that engineers can implement once, not twice.
- Focus order + SR semantics + ARIA budget decided before code.
- Reduces a11y rework cost by ≥60% vs post-build patching.
- Contrast + motion + target-size budgets baked into tokens.

## Applies If (ALL must hold)

- New component, page, or flow is being designed (pre-implementation).
- Team wants to avoid late-stage a11y rework.
- Design system tokens (colour, spacing, motion) are available.

## Skip If (ANY kills it)

- Component already implemented — use `a11y-testing` for retro audit.
- Pure visual refresh with no IA change — use design-token a11y check only.
- XR / spatial component — use `spatial-accessibility`, `vr-design-patterns`, `ar-design-patterns`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component / page brief | Markdown + low-fi | product |
| Design system tokens | color + spacing + motion tokens | design system |
| Target WCAG level | default 2.2 AA | team policy |
| User research notes | if available | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/05-examples.xml` | essential | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-spec.md` | Markdown skeleton for accessibility-first design spec. |
| `templates/focus-order.json` | JSON list of focus stops + return-focus targets. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility-first-design.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[wcag-22-compliance]]
- [[a11y-basics]]
- [[cognitive-inclusion-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
