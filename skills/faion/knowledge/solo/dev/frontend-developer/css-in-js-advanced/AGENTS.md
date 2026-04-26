# CSS-in-JS Advanced

## Summary

Zero-runtime CSS-in-JS (vanilla-extract, Panda CSS, StyleX) extracts styles at build time, producing plain CSS with no runtime serialization cost. Use `recipe()` for typed variants, `createVar()` for CSS variable contract, and Sprinkles for a constrained atomic utility layer. SSR style extraction for runtime libraries (styled-components, Emotion) requires a server-side registry and a FOUC Playwright assertion.

## Why

Runtime CSS-in-JS dominates LCP in large apps because the browser cannot paint until JS serializes and injects styles. Migrating to zero-runtime removes this bottleneck and makes components compatible with React Server Components. Sprinkles and Panda recipes encode the design token contract directly in TypeScript, making invalid token combinations a compile error.

## When To Use

- Migrating styled-components/Emotion to a zero-runtime solution for Core Web Vitals or RSC.
- Building a typed atomic CSS layer when Tailwind doesn't fit (heavy theming, multi-brand).
- Setting up SSR style extraction for a styled-components/Emotion app on Next.js Pages Router.
- Optimizing a runtime CSS-in-JS app whose LCP is dominated by serialized CSS injection.

## When NOT To Use

- New apps where Tailwind + CSS variables solves the problem — runtime CSS-in-JS adds cost without benefit.
- React Server Components-only trees: styled-components and Emotion require `'use client'`; pick vanilla-extract or StyleX.
- Component libraries published to npm — runtime CSS-in-JS forces consumers to ship the runtime too.

## Content

| File | What's inside |
|------|---------------|
| `content/01-vanilla-extract.xml` | recipe(), createVar(), styleVariants(), Sprinkles defineProperties — rules and examples. |
| `content/02-ssr-extraction.xml` | styled-components SSR registry for Next.js; FOUC assertion pattern; Emotion CacheProvider. |
| `content/03-antipatterns.xml` | styled.div inside render, prop-driven hot-path styles, missing defaultVariants, Sprinkles size explosion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/button.css.ts` | vanilla-extract recipe with color + size variants and createVar for focus color. |
| `templates/find-render-styled.sh` | Grep script to flag styled.X definitions inside React component render bodies. |

## Scripts

none
