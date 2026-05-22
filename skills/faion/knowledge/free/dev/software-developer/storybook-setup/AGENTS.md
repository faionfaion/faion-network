---
slug: storybook-setup
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Storybook v8/v9 setup for React component libraries: `main.
content_id: "a2a8771be488ea98"
tags: [storybook, react, csf3, chromatic, visual-regression]
---
# Storybook Setup

## Summary

**One-sentence:** Storybook v8/v9 setup for React component libraries: `main.

**One-paragraph:** Storybook v8/v9 setup for React component libraries: `main.ts` config, `preview.ts` global decorators (Theme, Router, ReactQuery), CSF3 story authoring (`StoryObj`, `args`, `argTypes`, `play` functions), MDX documentation, and Chromatic visual regression CI. Every story must include `tags: ['autodocs']` and `args` covering all required props.

## Applies If (ALL must hold)

- Bootstrapping a component library or design system in a React / Vue / Svelte / Angular codebase.
- Adding `*.stories.tsx` files alongside new components as part of a feature delivery.
- Generating MDX docs from existing components for non-developer stakeholders.
- Wiring visual regression (Chromatic / Percy) and a11y checks (`addon-a11y`) into CI.
- Building a sandbox for components that need to be reviewed before they are wired into the app.

## Skip If (ANY kills it)

- Single-page apps with fewer than ~10 components — overhead exceeds value.
- Framework-tightly-coupled components (e.g., relying on Next.js `app/` server components) where Storybook context is hard to fake.
- Pure backend / CLI projects.
- Internal-only "throwaway" admin UIs that won't be redesigned.
- When the team will not maintain stories — outdated stories are worse than none.

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

- parent skill: `free/dev/software-developer/`
