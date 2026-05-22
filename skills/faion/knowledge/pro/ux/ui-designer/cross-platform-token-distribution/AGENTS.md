---
slug: cross-platform-token-distribution
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A pipeline pattern for distributing design tokens from a single source (Tokens Studio / Figma) to multiple platform outputs — CSS variables, SCSS maps, iOS Swift, Android XML, React Native — using Style Dictionary as the transform engine.
content_id: "56e9659da11bd971"
tags: [design-tokens, style-dictionary, multi-platform, ci-drift-detection, design-systems]
---
# Cross-Platform Token Distribution

## Summary

**One-sentence:** A pipeline pattern for distributing design tokens from a single source (Tokens Studio / Figma) to multiple platform outputs — CSS variables, SCSS maps, iOS Swift, Android XML, React Native — using Style Dictionary as the transform engine.

**One-paragraph:** A pipeline pattern for distributing design tokens from a single source (Tokens Studio / Figma) to multiple platform outputs — CSS variables, SCSS maps, iOS Swift, Android XML, React Native — using Style Dictionary as the transform engine. Tokens are authored once and emitted per-platform via config-driven transforms; CI blocks merges when outputs drift from source.

## Applies If (ALL must hold)

- Setting up a multi-platform product (web + iOS + Android) with shared brand tokens.
- Migrating a web-only token set to cover native platforms.
- Adding CI gates that fail when generated platform outputs are stale relative to source.
- Auditing drift between Figma token export and shipped artifacts.

## Skip If (ANY kills it)

- Single-platform web-only products — Style Dictionary adds pipeline complexity with no payoff.
- Pre-design-system phase where the token contract is still unstable; pipeline churn exceeds value.
- Brand assets that change every campaign — distribution overhead exceeds reuse benefit.
- Closed mobile apps with a single developer who hand-edits XML — overhead exceeds saved minutes.

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

- parent skill: `pro/ux/ui-designer/`
