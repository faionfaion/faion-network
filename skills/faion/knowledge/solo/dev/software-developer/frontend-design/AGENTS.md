# Frontend Design

## Summary

A multi-phase workflow for solopreneur-scale UI projects: fix requirements, generate 3-5 truly distinct design variants (differing layout, not just colors), render them to screenshots, select one, refine it, scaffold Storybook with design tokens, and produce colocated components. Tokens come first; components inherit them.

## Why

Solopreneurs collapse designer + developer into one role. Without a diverge-then-converge process, the first idea ships. Generating variants forces comparison, and requiring each variant to differ in navigation pattern and information density kills lookalikes. Token-first prevents components from hardcoding colors that will need to change later.

## When To Use

- Greenfield frontend (landing, dashboard, marketing site) where visual direction is open.
- Component library bootstrap before product features land.
- Rebrand / redesign passes that need multiple explored variants before committing.
- Solopreneur projects where designer and dev are the same person and agents.
- Translating a brand brief into concrete tokens (colors, type scale, spacing) and components.

## When NOT To Use

- Active production UI with established design system — variant brainstorming is wasted; iterate on tokens instead.
- Pure backend or CLI projects.
- Brownfield refactors where scope is "make this page faster", not "redesign".
- Native mobile (iOS/Android) — patterns assume web; use platform-native tooling.
- Engineering-driven internal admin tools where utility outweighs aesthetics.

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Five-phase workflow: requirements, brainstorm, selection, Storybook, components; rules for variant distinctness and a11y gates. |
| `content/02-antipatterns.xml` | Antipatterns: tokens defined post-hoc, no a11y gate, LLM color hardcoding, Storybook version drift. |

## Templates

| File | Purpose |
|------|---------|
| (none) | No standalone template artifacts; scripts/ contains the render helper. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/render-variants.sh` | Playwright screenshots of all design variants at desktop + mobile, stitched into review grids. |
