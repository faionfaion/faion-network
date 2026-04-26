# Storybook Setup

## Summary

Storybook 8 with CSF 3 (`Meta<typeof Component>`, `StoryObj`, `tags: ['autodocs']`) wired to `@storybook/addon-a11y`, `@storybook/addon-interactions`, and Chromatic for visual regression. Stories co-located with components. `@storybook/test-runner` runs headless Playwright over all stories in CI. Every story must render without console errors before merge.

## Why

Storybook gives agents and designers a sandboxed component catalog with an args matrix for every variant. Combined with Chromatic visual snapshots and `addon-a11y`, it catches regressions that unit tests miss. The `test-runner` oracle makes CI pass/fail deterministic — without it, broken stories only surface during manual review.

## When To Use

- Initial Storybook 8.x install on Vite/Webpack/Next.js project.
- Wiring `.storybook/main.ts` and `.storybook/preview.ts` for theming, viewports, backgrounds, a11y addon.
- Adding visual, a11y, and interaction testing (Chromatic / test-runner / addon-a11y).
- Setting up CSF 3 stories and `tags: ['autodocs']` for a typed component library.

## When NOT To Use

- Project ships only one or two pages — Ladle boots faster with less config.
- No design system or shared component library yet — Storybook's value lives in component reuse.
- Team uses `playground/`-style Next.js dev pages and would duplicate that effort.

## Content

| File | What's inside |
|------|---------------|
| `content/01-configuration.xml` | main.ts (addons, framework, typescript options), preview.ts (decorators, globalTypes, backgrounds, viewports). |
| `content/02-story-authoring.xml` | CSF 3 shape, argTypes, play functions with userEvent, MDX docs blocks, autodocs tag rules. |
| `content/03-testing-ci.xml` | test-runner CI setup, Chromatic GH Action, a11y addon config, known Storybook 8 gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.ts` | Storybook main.ts with react-vite, essentials, interactions, a11y, Chromatic addon wired. |
| `templates/preview.ts` | preview.ts with theme globalType, background/viewport parameters, padding decorator. |
| `templates/storybook-ci.yml` | GitHub Actions workflow: build Storybook + run test-runner headless. |

## Scripts

none
