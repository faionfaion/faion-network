---
slug: css-in-js-basics
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Runtime CSS-in-JS (styled-components, Emotion) co-locates styles with React/Vue components and enables prop-driven dynamic styling via a typed ThemeProvider.
content_id: "198653e5ff838e69"
tags: [css-in-js, styled-components, emotion, theming, react]
---
# CSS-in-JS Basics

## Summary

**One-sentence:** Runtime CSS-in-JS (styled-components, Emotion) co-locates styles with React/Vue components and enables prop-driven dynamic styling via a typed ThemeProvider.

**One-paragraph:** Runtime CSS-in-JS (styled-components, Emotion) co-locates styles with React/Vue components and enables prop-driven dynamic styling via a typed ThemeProvider. Use when a project needs prop-driven dynamic styles that Tailwind cannot express ergonomically (e.g., arbitrary user-chosen colors, complex multi-brand theming). Without the DefaultTheme augmentation, theme is typed any and agents reach for inline hex values, defeating the design token contract. Transient props ($variant, $size) prevent prop leakage to the DOM. Pick one library per app — never mix runtimes.

## Applies If (ALL must hold)

- Component-driven React/Vue project where styles must travel with the component (open-source library, multi-app monorepo).
- Prop-driven dynamic styling requirement that Tailwind cannot express ergonomically (e.g., a color picker that injects arbitrary user-chosen colors).
- Theming requirement: light/dark plus brand white-label themes via ThemeProvider; ThemeProvider is cheaper to set up than runtime CSS variable plumbing.
- Onboarding a team familiar with styled-components or Emotion that does not yet need zero-runtime gains from zero-runtime CSS-in-JS libraries.

## Skip If (ANY kills it)

- React Server Components apps (Next.js App Router) where you want to keep most of the tree server-rendered — runtime CSS-in-JS forces 'use client' on every styled component. Use Tailwind, Panda, or vanilla-extract instead.
- Bundle-size-sensitive sites (landing pages, marketing pages) — styled-components alone adds ~12 KB gzipped runtime.
- Teams already standardized on Tailwind — mixing both CSS-in-JS and Tailwind creates two parallel design systems.
- Static sites generated to CDN — runtime CSS-in-JS leaves a small but real layout-shift window during hydration.

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
