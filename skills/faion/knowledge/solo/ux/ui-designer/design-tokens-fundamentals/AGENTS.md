---
slug: design-tokens-fundamentals
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three-tier design-token architecture (global → semantic → component) with named-by-intent semantics, single source of truth, and CI-enforced semantic-references-global rule so brand changes propagate in one commit.
content_id: "cab4ee38609b44a1"
complexity: deep
produces: spec
est_tokens: 4200
tags: ["design-tokens", "design-systems", "theming", "dark-mode", "css-variables"]
---
# Design Tokens Fundamentals

## Summary

**One-sentence:** Three-tier design-token architecture (global → semantic → component) with named-by-intent semantics, single source of truth, and CI-enforced semantic-references-global rule so brand changes propagate in one commit.

**One-paragraph:** Design tokens fail when they hold raw values, mix conventions, or live in two places. This methodology pins three tiers (global primitives → semantic aliases → component overrides), a single source of truth (Figma Variables OR a tokens JSON, not both), intent-based naming (color.feedback.error not color.red), and CI-enforced rules: no raw values in semantic tier, kebab-case throughout, generated outputs committed. Major version bumps gate breaking token renames.

**Ефективно для:**

- Solo founder bootstrapping a design system from scratch.
- Adding dark mode or white-label theming to an existing codebase.
- Migrating from Tailwind magic numbers to a governed token layer.
- AI agent consuming tokens.json to generate component CSS.

## Applies If (ALL must hold)

- A design system is being created OR a codebase is migrating to tokens.
- Dark mode, theme switching, or white-label is on the roadmap.
- A build step (Style Dictionary, Tailwind plugin, custom script) can ingest a tokens JSON.
- CI pipeline can run a lint step on token files.

## Skip If (ANY kills it)

- Single-component quick fix with no theming roadmap.
- Single-theme project with no dark mode planned.
- Figma and codebase already diverged irreconcilably — fix the divergence first.
- Legacy server-rendered project without a CSS variable pipeline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brand color + spacing scale | doc / Figma variables | Designer / brand guide |
| Build toolchain | Style Dictionary / Tailwind / custom | Frontend repo |
| Source-of-truth decision | string | ADR or design lead choice |
| CI pipeline access | yaml / config | Repo CI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/tailwind-design-tokens` | Tailwind-specific token bridge. |
| `solo/ux/handoff-spec-template` | Spec downstream consumes token references. |

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
| `draft-token-tiers` | sonnet | Per-tier judgement on tier assignment + aliasing. |
| `lint-tokens` | haiku | Deterministic Style Dictionary lint run. |
| `major-rename-impact-audit` | opus | Cross-consumer audit for breaking-rename impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-tokens-fundamentals.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/design-tokens-fundamentals.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens-fundamentals.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[tailwind-design-tokens]]
- [[handoff-spec-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
