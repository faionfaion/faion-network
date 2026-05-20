---
slug: practices-frontend-components
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four conventions for frontend component authoring: Storybook CSF3 stories co-located with components, design tokens as TypeScript constants (colors, spacing), a standardized co-located component file structure, and a 100-150 line CLAUDE.
content_id: "7f5be398be523bfb"
tags: [storybook, design-tokens, frontend, component-library, documentation]
---
# Frontend Component Authoring Practices

## Summary

**One-sentence:** Four conventions for frontend component authoring: Storybook CSF3 stories co-located with components, design tokens as TypeScript constants (colors, spacing), a standardized co-located component file structure, and a 100-150 line CLAUDE.

**One-paragraph:** Four conventions for frontend component authoring: Storybook CSF3 stories co-located with components, design tokens as TypeScript constants (colors, spacing), a standardized co-located component file structure, and a 100-150 line CLAUDE.md skeleton for AI-readable folder documentation.

## Applies If (ALL must hold)

- Adding a new component to a React component library — use as the file layout template.
- Setting up Storybook for the first time in a project.
- Creating or updating design tokens for a project's visual system.
- Generating CLAUDE.md/AGENTS.md documentation for any project folder.

## Skip If (ANY kills it)

- React application components that are not part of a shared library — a loose component in an app page does not need a Storybook story.
- Storybook v8/v9 with `tags: ['autodocs']` and new args API — this covers v7 CSF3 basics only.
- Design system theming with CSS custom properties or CSS-in-JS tokens — covers TypeScript-only tokens.

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

- parent skill: `solo/dev/automation-tooling/`
