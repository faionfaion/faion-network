# Agent Integration — CSS-in-JS Basics

## When to use
- Component-driven React/Vue project where styles must travel with the component (open-source library, multi-app monorepo).
- Need prop-driven dynamic styling that Tailwind can't express ergonomically (e.g., a color picker that injects arbitrary user-chosen colors).
- Theming requirement: light/dark plus brand white-label themes — `ThemeProvider` is cheaper to set up than runtime CSS variable plumbing.
- Onboarding a team familiar with styled-components / Emotion that doesn't yet need zero-runtime gains.

## When NOT to use
- React Server Components apps (Next.js App Router) where you want to keep most of the tree server-rendered — runtime CSS-in-JS forces `'use client'`. Use Tailwind, Panda, or vanilla-extract instead.
- Bundle-size-sensitive sites (landing pages, marketing) — styled-components alone adds ~12 KB gzipped runtime.
- Teams already standardized on Tailwind — mixing both creates two parallel design systems.
- Static sites generated to CDN — runtime CSS-in-JS leaves a small but real layout-shift window during hydration.

## Where it fails / limitations
- Transient props: writing `<Button variant="primary">` instead of `<Button $variant="primary">` leaks the prop to the DOM (`<button variant="primary">`), causing console warnings.
- Theming: `theme` prop is `any` by default in styled-components — agents skip the `DefaultTheme` declaration and lose typesafety.
- SSR style flash: skipping the SSR registry causes FOUC on first paint; reproducible only on slow networks, easy to miss in dev.
- Re-renders: prop-driven dynamic styles re-serialize the CSS string on every render unless transient props + `shouldForwardProp` are used.
- Source maps: stack traces from styled-components show display names like `Styled(div)` unless `babel-plugin-styled-components` is configured.

## Agentic workflow
For new components, drive the agent with the prop spec + theme contract; let it produce a typed styled component, a `defaultProps`, and a Storybook story exercising every variant. For existing codebases, run a subagent in audit mode that flags non-transient props, runtime styled definitions inside render bodies, and missing SSR setup. Keep humans in the loop for the theme contract — that becomes the project's de facto design API and is hard to refactor.

### Recommended subagents
- `faion-feature-executor` — small per-component tasks (convert one Tailwind component to styled-components, or add a variant) with build + visual gate.
- `faion-sdd-executor-agent` — when introducing CSS-in-JS for the first time, the spec/design loop forces you to pick a single library.

### Prompt pattern
- "Write a `<Button>` styled-components implementation matching this Figma spec. Use a typed theme (`DefaultTheme`), transient props (`$variant`, `$size`), and `as` polymorphism. Output `Button.tsx` plus `theme.ts` augmenting `styled-components`."
- "Audit `src/components/**/*.tsx` for: (1) styled definitions inside render, (2) non-transient props leaking to DOM, (3) missing `as` typing. Return a refactor list, do not edit yet."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm add styled-components` | Runtime CSS-in-JS | https://styled-components.com |
| `pnpm add -D babel-plugin-styled-components` | Display names + dead-code elim + SSR | https://styled-components.com/docs/tooling#babel-plugin |
| `pnpm add @emotion/react @emotion/styled` | Emotion runtime CSS-in-JS | https://emotion.sh/docs/introduction |
| `pnpm add -D @emotion/babel-plugin` | Source maps + label | https://emotion.sh/docs/@emotion/babel-plugin |
| `npx eslint --rule "react/no-unknown-property: error"` | Catch unknown DOM props from non-transient styled-components | https://eslint.org/docs/latest/rules/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | Yes | Author stories per variant; agent generates them from the prop type. |
| Chromatic | SaaS | Yes | Visual regression on every story — catches CSS-in-JS regressions early. |
| Bundlephobia | SaaS | Partial | Use to compare runtime bundle costs (styled-components vs Emotion vs vanilla-extract). |
| Figma Tokens | SaaS plugin | Yes | Export tokens to JSON; agent maps them onto the `DefaultTheme`. |

## Templates & scripts
See `templates.md` for the styled-components Button + theme contract. Type-augment snippet (the line agents forget):

```ts
// types/styled.d.ts
import 'styled-components';
declare module 'styled-components' {
  export interface DefaultTheme {
    colors: { primary: string; secondary: string; focus: string; bg: string; fg: string };
    space: { sm: string; md: string; lg: string };
    radii: { sm: string; md: string };
  }
}
```

```ts
// scripts/check-transient-props.mjs
// Flag styled.X<Props> definitions where a prop name doesn't start with $
import { execSync } from 'node:child_process';
const grep = "grep -rEn 'styled\\.[a-zA-Z]+<\\{[^$]' src --include='*.tsx' || true";
const out = execSync(grep, { encoding: 'utf8' });
if (out) { console.error('Non-transient props detected:\n' + out); process.exit(1); }
console.log('OK');
```

## Best practices
- Always use transient props (`$variant`) in styled-components. Plain prop names leak to the DOM and trigger React warnings.
- Define one source of truth for the theme: a `theme.ts` + a `DefaultTheme` declaration. Never inline color hex inside styled blocks.
- Pick one library per app. Mixing styled-components and Emotion compiles both runtimes into the bundle.
- For components shipped to npm, prefer Emotion's `css` prop or zero-runtime — consumers shouldn't be forced to install styled-components.
- Add the Babel plugin in dev — display names make DevTools usable; dead-code elim shrinks production bundle.

## AI-agent gotchas
- LLMs default to non-transient props (`variant` instead of `$variant`); requires a lint rule or explicit prompt instruction.
- Agents copy SSR setup from Pages Router examples into App Router and break — App Router needs a `'use client'` registry component, not `_document.tsx`.
- The `theme` parameter inside template literals is typed `any` without the augmentation file; agents reach for `as any` to silence errors.
- Generated `styled(Component)` calls drop refs unless the inner component is `forwardRef` — agents rarely add the wrapper.
- `as` polymorphism: agents type `as: 'a' | 'button'` but forget that styled-components actually accepts component types too; lose flexibility.
- Asked to "make this dynamic", LLMs add a `styled.div` inside the function body — every render creates a new component class. Lint or block in review.

## References
- styled-components — https://styled-components.com/docs
- Emotion — https://emotion.sh/docs/introduction
- TypeScript theme typing — https://styled-components.com/docs/api#typescript
- `babel-plugin-styled-components` — https://styled-components.com/docs/tooling
- Mark Dalgleish, "Slow death of CSS-in-JS" (history + tradeoffs) — https://dev.to/srmagura/why-were-breaking-up-wiht-css-in-js-4g9b
