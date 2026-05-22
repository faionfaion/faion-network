---
slug: css-in-js-advanced
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Zero-runtime CSS-in-JS (vanilla-extract, Panda CSS, StyleX) extracts styles at build time, producing plain CSS with no runtime serialization cost.
content_id: "7d13ec4e88e8c6d2"
tags: [css-in-js, vanilla-extract, zero-runtime, ssr, styled-components]
---
# CSS-in-JS Advanced

## Summary

**One-sentence:** Zero-runtime CSS-in-JS (vanilla-extract, Panda CSS, StyleX) extracts styles at build time, producing plain CSS with no runtime serialization cost.

**One-paragraph:** Zero-runtime CSS-in-JS (vanilla-extract, Panda CSS, StyleX) extracts styles at build time, producing plain CSS with no runtime serialization cost. Use recipe() for typed variants, createVar() for CSS variable contract, and Sprinkles for a constrained atomic utility layer. SSR style extraction for runtime libraries (styled-components, Emotion) requires a server-side registry and a FOUC Playwright assertion.

## Applies If (ALL must hold)

- Migrating styled-components / Emotion codebase to a zero-runtime solution (vanilla-extract, Linaria, Panda CSS, StyleX) for Core Web Vitals or React Server Components.
- Building a typed atomic CSS layer (Sprinkles / Panda recipes) when Tailwind doesn't fit (e.g., heavy theming, multi-brand white-label).
- Setting up SSR style extraction for a styled-components / Emotion app on Next.js Pages Router or Remix.
- Optimizing a runtime CSS-in-JS app whose Largest Contentful Paint is dominated by serialized CSS injection.

## Skip If (ANY kills it)

- New apps where Tailwind + CSS variables solves the problem — runtime CSS-in-JS adds bundle and hydration cost without theming gains.
- React Server Components-only trees: styled-components and Emotion runtime require a 'use client' boundary; pick vanilla-extract, Panda, or StyleX instead.
- Component libraries published to npm — runtime CSS-in-JS forces the consumer's bundler to ship the runtime; ship plain CSS or zero-runtime output.

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

- parent skill: `solo/dev/frontend-developer/`
