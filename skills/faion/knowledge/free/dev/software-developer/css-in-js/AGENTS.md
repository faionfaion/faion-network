# CSS-in-JS

## Summary

A methodology for applying CSS-in-JS in React projects: use zero-runtime libraries (`vanilla-extract`, `linaria`, `panda-css`) for RSC / SSR builds; runtime libraries (`styled-components` v6, `@emotion/styled`) only for client-only SPAs. Define styled components at module scope (never inside the function body), use transient props (`$variant`), co-locate tokens with TypeScript augmentation, and extract critical CSS for SSR to prevent FOUC.

## Why

Runtime CSS-in-JS is incompatible with React Server Components and adds 10-30 KB of runtime overhead before any component styles. Defining `styled.X` inside render creates a new class on every render, causing class explosion and performance degradation. Without `$transient` props, style props leak to the DOM. Without TypeScript theme augmentation, token typos are undetected. These failures are silent until production.

## When To Use

- React or Vue components with truly dynamic styles computed from runtime props/state.
- Design systems where tokens need TS-typed access from inside components.
- A11y-driven theming (dark mode, high-contrast, prefers-reduced-motion).
- Component libraries shipped to npm expecting zero CSS-import setup.
- Migrating from inline `style={}` blobs to scoped maintainable styles.

## When NOT To Use

- Next.js 15 / RSC App Router: runtime CSS-in-JS breaks Server Components — use Tailwind, CSS Modules, or `vanilla-extract`.
- Static marketing sites where CSS Modules or plain CSS ship less JS.
- Tailwind-standardized teams — mixing creates a split design system.
- Embedded / size-constrained bundles (extension popups, AMP, email).
- React Native — use StyleSheet API; CSS-in-JS libs that map onto RN carry maintenance risk.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Zero-runtime vs runtime selection rule, module-scope rule, transient props rule, theme augmentation rule, SSR wiring rule |
| `content/02-examples.xml` | styled-components Button with variants, theme setup, ThemeProvider, Emotion css prop |
| `content/03-antipatterns.xml` | Antipatterns: styled inside render, missing transient props, missing DefaultTheme augment, runtime CSS-in-JS in RSC |

## Templates

| File | Purpose |
|------|---------|
| `templates/css-in-js-detect.sh` | Detects RSC/RN/Vite context and recommends safe CSS-in-JS lib or rejects runtime libs |
