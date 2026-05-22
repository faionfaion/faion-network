---
slug: storybook-setup
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Storybook 8 with CSF 3 (Meta<typeof Component>, StoryObj, tags: ['autodocs']) wired to @storybook/addon-a11y, @storybook/addon-interactions, and Chromatic for visual regression.
content_id: "a2a8771be488ea98"
tags: [storybook, csf3, component-testing, visual-regression, accessibility]
---
# Storybook Setup

## Summary

**One-sentence:** Storybook 8 with CSF 3 (Meta<typeof Component>, StoryObj, tags: ['autodocs']) wired to @storybook/addon-a11y, @storybook/addon-interactions, and Chromatic for visual regression.

**One-paragraph:** Storybook 8 with CSF 3 (Meta<typeof Component>, StoryObj, tags: ['autodocs']) wired to @storybook/addon-a11y, @storybook/addon-interactions, and Chromatic for visual regression. Stories co-located with components. @storybook/test-runner runs headless Playwright over all stories in CI. Every story must render without console errors before merge.

## Applies If (ALL must hold)

- Initial Storybook 8.x install on Vite/Webpack/Next.js project.
- Wiring .storybook/main.ts and .storybook/preview.ts for theming, viewports, backgrounds, a11y addon.
- Adding visual, a11y, and interaction testing (Chromatic / test-runner / addon-a11y).
- Setting up CSF 3 stories and tags: ['autodocs'] for a typed component library.

## Skip If (ANY kills it)

- Project ships only one or two pages — Ladle boots faster with less config.
- No design system or shared component library yet — Storybook's value lives in component reuse.
- Team uses playground/-style Next.js dev pages and would duplicate that effort.

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
