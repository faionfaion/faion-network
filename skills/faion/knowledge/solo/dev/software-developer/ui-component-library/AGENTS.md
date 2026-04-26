# UI Component Library

## Summary

Versioned, semver-controlled React component library with a layered structure (primitives → composite → patterns → layout), consistent prop API doctrine, design token integration, co-located Storybook stories + tests, and Radix UI/React Aria for interactive primitives. Distinct from the shadcn copy-paste model — this methodology produces a packaged library.

## Why

A shared library enforces API consistency, accessibility, and token usage across multiple apps in a monorepo. Without a library, each app reimplements the same Button/Modal/Input with slight API differences, creating inconsistency and compounding accessibility debt. Co-locating tests and stories with each component ensures regressions are caught immediately.

## When To Use

- Multi-app monorepo that needs shared, versioned UI components (web, admin, mobile-web)
- Enforcing accessibility, theming, and prop API consistency via code review and audits
- Need semver-controlled exports consumed by multiple packages

## When NOT To Use

- Single small app with no plans to share components — premature extraction adds overhead
- Heavy bespoke-per-page styling with low reuse (marketing landing pages, one-off campaigns)
- Replacing well-maintained external libraries (MUI, Mantine) without a clear extension story
- Team cannot commit to maintaining stories, tests, and tokens — the library will rot

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | API doctrine, token rules, accessibility requirements, bundle rules, semver discipline |
| `content/02-examples.xml` | Button and Input component examples with forwardRef, variants, ARIA, and CSS modules |

## Templates

| File | Purpose |
|------|---------|
| `templates/new-component.sh` | Scaffold component folder with .tsx, .module.css, .stories.tsx, barrel export |
