# Storybook Setup

## Summary

Storybook v8/v9 setup for React component libraries: `main.ts` config, `preview.ts` global decorators (Theme, Router, ReactQuery), CSF3 story authoring (`StoryObj`, `args`, `argTypes`, `play` functions), MDX documentation, and Chromatic visual regression CI. Every story must include `tags: ['autodocs']` and `args` covering all required props.

## Why

Agents generate stories from stale training data (v6 argTypes syntax, `@storybook/jest` instead of `@storybook/test`, wrong framework for Next.js). Without explicit story requirements (one story per visual variant, `play` function for interactions, `autodocs` tag), the Controls panel and visual test suite are unusable. Outdated stories are worse than no stories.

## When To Use

- Bootstrapping a component library or design system in a React codebase.
- Adding `*.stories.tsx` alongside new components as part of feature delivery.
- Generating MDX docs from existing components for designer review.
- Wiring visual regression (Chromatic) and a11y checks (`addon-a11y`) into CI.
- Building an isolated sandbox for components that need sign-off before app wiring.

## When NOT To Use

- Single-page apps with fewer than ~10 components — overhead exceeds value.
- Next.js App Router server components — Storybook context is hard to fake.
- Pure backend / CLI projects.
- Internal-only throwaway admin UIs that will not be redesigned.
- Teams that will not maintain stories — outdated stories are worse than none.

## Content

| File | What's inside |
|------|---------------|
| `content/01-configuration.xml` | `main.ts` config rules, `preview.ts` decorator patterns, addon list, TypeScript docgen setup. |
| `content/02-story-authoring.xml` | CSF3 rules: `StoryObj`, `args`, `argTypes`, `play` function, MDX documentation structure. |
| `content/03-testing-and-ci.xml` | Interaction testing, Chromatic visual regression, a11y testing, CI workflow pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.ts` | Storybook v8 `main.ts` with essentials, interactions, a11y, Chromatic addons. |
| `templates/preview.ts` | Global preview with theme, ReactQuery, router decorators and viewport config. |
| `templates/story.stories.tsx` | CSF3 story template with `autodocs`, `argTypes`, variants, and `play` function. |
