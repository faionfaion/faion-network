---
slug: storybook-setup
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Storybook v8/v9 setup for React: main.ts + preview.ts, CSF3 stories with args + play, Chromatic visual regression.
content_id: "a2a8771be488ea98"
complexity: medium
produces: code
est_tokens: 3500
tags: [storybook, react, csf3, chromatic, visual-regression]
---
# Storybook Setup

## Summary

**One-sentence:** Storybook v8/v9 setup for React: main.ts + preview.ts, CSF3 stories with args + play, Chromatic visual regression.

**One-paragraph:** Storybook v8/v9 setup for React component libraries: main.ts config, preview.ts global decorators (Theme, Router, ReactQuery), CSF3 story authoring (StoryObj, args, argTypes, play functions), MDX documentation, and Chromatic visual regression CI. Every story includes tags: ['autodocs'] and args covering all required props.

**Ефективно для:** frontend-інженера, який бутстрапить компонентну бібліотеку — закриває петлю між сирими React-компонентами і живою документацією + visual-regression CI.

## Applies If (ALL must hold)

- Bootstrapping a component library or design system.
- Adding *.stories.tsx files alongside new components.
- Wiring Chromatic visual regression CI.
- Authoring MDX documentation for design tokens or guidelines.

## Skip If (ANY kills it)

- Pages-only Next.js apps with no shared components.
- Backend or CLI project — Storybook is for UI.
- Pure CSS work — use a styleguide tool instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| React 18+ project | package.json | repo root |
| Storybook v8 or v9 installed | package | npx storybook@latest init |
| Component to document | tsx | src/components/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/typescript-strict-mode` | Story args/argTypes rely on accurate TS types. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: CSF3 with satisfies Meta, autodocs tag, args cover required props, global decorators in preview.ts, Chromatic in CI. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: main.ts + preview.ts + per-component <Component>.stories.tsx with default Meta + named StoryObj entries + Chromatic CI step. Forbidden: CSF2 stories, args missing required props. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: CSF2 syntax, missing autodocs, args without required props, Chromatic skipped. | ~700 |
| `content/04-procedure.xml` | medium | Steps: storybook init → configure main.ts → wire preview.ts decorators → author <Component>.stories.tsx → add Chromatic CI. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: pure component? → static stories. Stateful? → play function. Visual regression matters? → Chromatic. Else: docs only. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-story-file` | haiku | Template fill from component props. |
| `author-play-function` | sonnet | Interactive story with judgement on user flow. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.storybook/main.ts` | Storybook v9 main config: stories glob, addons, framework. |
| `templates/.storybook/preview.ts` | Global decorators (Theme, Router, ReactQuery). |
| `templates/Component.stories.tsx` | CSF3 story: Meta + Default + variants + play function. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-storybook-setup.py` | Check every component has a .stories.tsx; autodocs tag present; args cover required props. | Pre-commit and on component add. |

## Related

- [[typescript-strict-mode]]
- [[tailwind]]
- [[testing]]

## Decision tree

The tree at content/06-decision-tree.xml decides static stories vs play functions, Chromatic vs no visual regression, and MDX docs vs autodocs. Walk it whenever a new component is added.
