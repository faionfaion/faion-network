# CSS-in-JS Basics

## Summary

CSS-in-JS (styled-components, Emotion) co-locates styles with components and enables prop-driven dynamic styling via a typed `ThemeProvider`. Transient props (`$variant`, `$size`) must be used in styled-components to prevent prop leakage to the DOM. One library per app — never mix runtimes. Define a `DefaultTheme` declaration file to get TypeScript safety inside template literals.

## Why

Runtime CSS-in-JS is the right tradeoff when a project needs prop-driven dynamic styles that Tailwind cannot express ergonomically (e.g., arbitrary user-chosen colors, complex multi-brand theming). Without the `DefaultTheme` augmentation, `theme` is typed `any` and agents reach for inline hex values, defeating the design token contract.

## When To Use

- Component-driven React/Vue project where styles must travel with the component.
- Prop-driven dynamic styling that Tailwind cannot express ergonomically.
- Theming requirement: light/dark plus brand white-label themes via ThemeProvider.
- Team familiar with styled-components/Emotion that does not yet need zero-runtime gains.

## When NOT To Use

- React Server Components apps (Next.js App Router) — runtime CSS-in-JS forces `'use client'`; use Tailwind or vanilla-extract.
- Bundle-size-sensitive sites — styled-components adds ~12 KB gzipped runtime.
- Teams already standardized on Tailwind — mixing creates two parallel design systems.
- Static CDN sites — runtime CSS-in-JS leaves a layout-shift window during hydration.

## Content

| File | What's inside |
|------|---------------|
| `content/01-styled-components.xml` | Transient props rule, typed variants via css helper, theme contract, DefaultTheme declaration. |
| `content/02-emotion.xml` | css prop jsxImportSource, styled approach, composition with css(), Emotion-specific gotchas. |
| `content/03-antipatterns.xml` | styled.X inside render, non-transient DOM leakage, missing SSR registry, mixing libraries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/styled.d.ts` | DefaultTheme declaration — the augmentation file agents routinely forget. |
| `templates/check-transient-props.mjs` | Script to flag styled.X definitions with non-transient props. |

## Scripts

none
