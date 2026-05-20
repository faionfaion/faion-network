---
slug: storybook-as-source-of-truth
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "9c3770b6ee29fd0f"
summary: Codifies Storybook as the canonical Source of Truth for a design system — story-per-state discipline, a11y addon enforcement, token-first composition, and the tokens → Storybook → Figma library → PR governance loop.
tags: [storybook, design-system, ux, frontend, a11y, pro, dev]
---
# Storybook as Source of Truth

## Summary

**One-sentence:** Establishes Storybook as the canonical Source of Truth (SoT) for a design system, with mandatory story-per-state coverage, the a11y addon as a CI gate, and a tokens → Storybook → Figma library → PR governance loop.

**One-paragraph:** Most teams ship Storybook and stop there — it becomes a stale documentation site. This methodology converts Storybook into the SoT for the design system: every visual state of every component is encoded as a story, the a11y addon runs in CI, design tokens are the only colour/spacing/typography source, and Figma libraries are generated FROM Storybook (not the other way around). Storybook becomes the artifact that PRs are reviewed against, the Figma sync happens via Storybook addons, and any deviation in product code is a PR comment, not a discussion. Pairs with the design-system contribution model (PR governance for new components).

## Applies If (ALL must hold)

- Codebase has a shared design system used across ≥2 product surfaces (or planned to within 1 quarter).
- A frontend framework with Storybook 8+ support (React, Vue, Angular, Svelte, Lit, web components).
- Design tokens exist OR can be defined as the first migration step (Style Dictionary, design-tokens JSON, CSS custom properties).
- Team has CI capable of running headless story builds and the a11y addon.

## Skip If (ANY kills it)

- Single-app project with no plan for reuse — Storybook becomes maintenance debt without a payoff.
- Team owns no design tokens and cannot get them defined — adopting Storybook without tokens makes it a screenshot gallery.
- Design lead refuses to treat Storybook as the SoT (Figma remains canonical) — political prerequisite is missing; resolve before adoption.
- Tooling forbids open-source dependencies large enough to host Storybook (rare; flagged here for compliance contexts).

## Prerequisites

- Storybook 8+ installed with the framework's official integration.
- Design tokens defined in a single file/package (e.g. `@my-org/tokens`) imported by component CSS.
- The `@storybook/addon-a11y` installed.
- A CI job that runs `storybook build` + `test-storybook` (or play-function tests) on every PR.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux-ui-designer/design-tokens-architecture` (if present) | Token model is the upstream input. |
| `pro/dev/software-developer/component-library-versioning` (if present) | Versioning policy for the SoT package. |
| `geek/dev/software-developer/fitness-function-suite-bootstrap` | A11y addon results feed into fitness functions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: story-per-state, a11y addon CI gate, tokens-only styling, Figma generated from Storybook, deviation = PR comment | ~1300 |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodologies: `audit-grade-api-design`, `audit-grade-code-review-checklist`
- external: [Storybook 8 Docs](https://storybook.js.org/) · [Storybook a11y Addon](https://storybook.js.org/addons/@storybook/addon-a11y) · [Style Dictionary](https://amzn.github.io/style-dictionary/) · [Design Tokens W3C Community Group](https://www.designtokens.org/)
