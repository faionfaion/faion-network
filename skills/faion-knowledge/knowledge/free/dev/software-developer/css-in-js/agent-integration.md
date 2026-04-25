# Agent Integration — CSS-in-JS Basics

## When to use
- React or Vue components with truly **dynamic** styles (computed from runtime props/state, theme switches, user-customizable design systems).
- Building or extending a design system where tokens (colors, spacing, radii) need TS-typed access from inside components.
- A11y-driven theming (dark mode, high-contrast, prefers-reduced-motion) where conditional CSS needs JavaScript context.
- Component libraries shipped to npm where consumers expect zero CSS-import setup (`styled-components`, `@emotion/styled`).
- Migrating from inline `style={}` blobs to a maintainable scoped-style approach without rewriting in CSS Modules.

## When NOT to use
- New 2025/2026 projects on Next.js 15 / RSC where runtime CSS-in-JS (`styled-components` v6 with classic transform, `@emotion/react`) is **not supported in Server Components**. Use Tailwind, CSS Modules, or zero-runtime CSS-in-JS (`vanilla-extract`, `linaria`, `panda-css`) instead.
- Static marketing sites where CSS Modules or plain CSS ship less JS.
- Teams already standardized on Tailwind — mixing pulls the design system in two directions.
- Embedded / size-constrained bundles (extension popups, AMP, email): runtime CSS-in-JS adds 10-30 KB gz before any styles.
- React Native — RN has its own StyleSheet API; CSS-in-JS libs that map onto it (e.g., styled-components/native) carry maintenance risk.

## Where it fails / limitations
- **RSC incompatibility.** `styled-components` and Emotion's runtime require client components; agents that wrap a Server Component break the build silently or produce hydration mismatches.
- **Bundle bloat.** Runtime engine + per-component generated CSS doubles initial CSS payload vs. Tailwind / CSS Modules for many real apps.
- **Render cost.** Computing styles per render on prop changes is non-trivial; misuse (defining `styled.div` inside the function body) causes infinite re-renders or class explosion.
- **Style invalidation.** Theme changes re-render every styled component; large trees stutter on theme toggle without `React.memo`.
- **Type-safety theater.** TypeScript augmentation for `DefaultTheme` is verbose; without it, `theme.colors.foo` typos go undetected.
- **SSR / streaming.** Each library has its own SSR wiring (`ServerStyleSheet`, `extractCriticalToChunks`, `cache`); agents copy snippets that don't match the framework.
- **`!important` and CSS specificity wars** with global stylesheets (Tailwind, Bootstrap) — generated class names are harder to override deterministically.
- **`css` prop type errors in TS** require Babel plugin or JSX pragma config; agents miss this and ship JSX that fails to compile.
- **Vendor prefixing**, container queries, `:has()`, `@layer` — newer CSS features may lag in older runtime engines.

## Agentic workflow
Use Claude subagents in three modes. (1) **Selector** — given the project (framework version, target runtime), the agent picks the correct CSS-in-JS variant: zero-runtime (`vanilla-extract`, `linaria`, `panda-css`) for RSC, runtime (`styled-components`, `@emotion`) for client-only SPAs, or rejects CSS-in-JS in favor of Tailwind/CSS Modules. (2) **Tokenizer** — generates `theme/tokens.ts` from a design spec (Figma export, brand JSON), wires `ThemeProvider`, and emits the TS module augmentation. (3) **Component-builder** — produces typed styled components from a UI spec (props, variants, states) and pairs each with a Storybook story and Vitest snapshot. A reviewer agent flags `styled.X` defined inside render, missing `$transient` props, and use in Server Components.

### Recommended subagents
- A purpose-built **css-in-js-selector agent** (worth creating): inspects `package.json`, `next.config.js`, and tsconfig to recommend the correct lib; refuses runtime CSS-in-JS when RSC is detected.
- A purpose-built **theme-token agent** (worth creating): consumes a Figma JSON or a design tokens spec and emits `theme.ts` + `styled.d.ts` augmentation + a `<ThemeProvider>` wrapper.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — gates UI PRs against the design system spec; rejects components without Storybook coverage.
- `password-scrubber-agent` — relevant only when sharing tokens externally that may include client-specific brand secrets.

### Prompt pattern
Lib-pick pass:
```
Inspect package.json and framework config in <repo>. Decide:
- If Next.js >=13 with App Router: prefer vanilla-extract or panda-css.
- If Vite SPA / CRA: styled-components or Emotion are fine.
- If RN: react-native StyleSheet or restyle, NOT runtime CSS-in-JS.
Output: chosen lib, rationale (3 bullets), risks, install commands,
and required SSR wiring snippets if any.
```

Component pass:
```
Build <ComponentName> with styled-components v6:
- Variants: <list>
- Sizes: sm/md/lg
- States: hover, focus-visible, disabled, active
- Use $transient props (e.g. $variant, $size).
- Theme tokens from theme/theme.ts.
- Include Storybook story with controls for variant/size/disabled.
- Snapshot test (vitest + @testing-library/react).
Reject: defining styled inside render, theme typos, hardcoded colors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vanilla-extract` | Zero-runtime CSS-in-TS, RSC-safe | `pnpm add @vanilla-extract/css` ; https://vanilla-extract.style |
| `panda-css` | Build-time atomic CSS-in-JS | `pnpm add @pandacss/dev` ; https://panda-css.com |
| `linaria` | Zero-runtime CSS-in-JS, ESM | `pnpm add @linaria/core @linaria/react` ; https://linaria.dev |
| `styled-components` v6 | Runtime CSS-in-JS (with Babel transformer for RSC partial support) | https://styled-components.com |
| `@emotion/react` + `@emotion/styled` | Runtime CSS-in-JS, lightweight | https://emotion.sh |
| `stylelint` + `stylelint-config-styled-components` | Linting CSS in template literals | https://stylelint.io |
| `babel-plugin-styled-components` / `@compiled` | SSR + dev-tooling for styled-components / Atlassian Compiled | https://github.com/atlassian-labs/compiled |
| `style-dictionary` | Convert design tokens → multi-platform output | https://amzn.github.io/style-dictionary/ |
| `figma-tokens` (Tokens Studio plugin + CLI) | Pull tokens from Figma | https://docs.tokens.studio |
| `bundlemon` / `size-limit` | Track CSS-in-JS runtime overhead in CI | https://github.com/ai/size-limit |
| `eslint-plugin-react`, `eslint-plugin-styled-components-a11y` | Lint generated styles | https://www.npmjs.com/package/eslint-plugin-styled-components-a11y |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | yes (CLI + Story Index API) | Mandatory for component preview; agents can scaffold stories from styled component types. |
| Chromatic | SaaS visual regression | yes (CLI) | Catches CSS-in-JS regressions human review misses (subpixel, theme variants). |
| Tokens Studio (Figma plugin) | SaaS | partial | Pull design tokens via JSON; agents transform with style-dictionary. |
| Style Dictionary | OSS CLI | yes | Pipeline output: TS, CSS variables, SCSS, native StyleSheet. |
| Panda CSS Studio | OSS dev tool | yes | Visualize generated atomic classes during agent generation. |
| Vercel / Netlify | SaaS | yes | Deploy preview catches RSC + runtime CSS-in-JS incompatibilities at build. |
| Compiled by Atlassian | OSS | yes | Build-time CSS-in-JS with React typings; agent-friendly. |
| Linaria CLI | OSS | yes | Compiles tagged template literals to atomic CSS at build. |

## Templates & scripts

The README ships per-library examples; the missing piece for agents is a **lib-detector** that decides whether the project is RSC-safe. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# css-in-js-detect.sh — recommend a CSS-in-JS strategy for a JS/TS repo.
set -euo pipefail
root="${1:-.}"
[ -f "$root/package.json" ] || { echo "no package.json in $root"; exit 1; }
node - <<'JS' "$root"
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const root = process.argv[1];
const pkg = JSON.parse(readFileSync(join(root,'package.json'),'utf8'));
const dep = { ...(pkg.dependencies||{}), ...(pkg.devDependencies||{}) };
const has = (n) => n in dep;
const rsc = (has('next') && /14|15|^>=?13/.test(dep.next||'')) || existsSync(join(root,'app/layout.tsx'));
const rn  = has('react-native');
const vite = has('vite');
const recs = [];
if (rn)        recs.push('react-native StyleSheet or @shopify/restyle');
else if (rsc)  recs.push('vanilla-extract OR panda-css OR Tailwind (RSC-safe). Avoid styled-components/Emotion runtime.');
else if (vite) recs.push('styled-components v6 or @emotion/react are fine.');
else           recs.push('CSS Modules + Tailwind unless dynamic styling required.');
const risks = [];
if (rsc && (has('styled-components') || has('@emotion/styled')))
  risks.push('runtime CSS-in-JS detected with App Router — likely RSC breakage');
if (has('styled-components') && has('@emotion/styled'))
  risks.push('two CSS-in-JS engines installed — pick one');
console.log(JSON.stringify({ recommendations: recs, risks }, null, 2));
JS
```

Hook into `pre-commit` or run ad-hoc; the agent reads the JSON and acts.

## Best practices
- **Define `styled.X` at module scope.** Never inside the component function — class explosion + re-renders.
- **Use transient props (`$variant`, `$size`).** Standard props leak to the DOM and trigger React warnings.
- **Co-locate tokens with TypeScript augmentation.** A typed theme prevents 90% of "color undefined" bugs.
- **Memoize variant tables** outside the component body so `css\`\`` blocks are stable references.
- **Extract critical CSS for SSR** in client-only frameworks; without it, FOUC on first paint.
- **Prefer zero-runtime libs** (`vanilla-extract`, `linaria`, `panda-css`) for SSR/RSC builds; runtime CSS-in-JS is a 2017 pattern aging out.
- **Cap dynamic interpolations.** If a single component has >10 `${theme...}` reads, refactor to CSS variables exposed by the theme provider.
- **Test theme switching** via `@testing-library/react` with both providers; toggling missed theme keys often only show in dark mode.
- **Lint banned patterns** (`color: red`, hardcoded hex codes, `!important`, `:hover` without `:focus-visible`) with stylelint inside template literals.
- **Track CSS-in-JS bundle weight.** Add `size-limit` for both runtime + generated styles; alert on +5 KB gzip per release.
- **Server-safe pragma** — for RSC partial support, mark interactive style branches with `'use client'` files only and keep static markup in Server Components using Tailwind/Modules.

## AI-agent gotchas
- **Default LLM output picks `styled-components`.** Models trained on 2019-2022 React tutorials emit it by default; in 2026 Next.js App Router that's broken. Always pin the prompt to the framework + RSC awareness.
- **`styled.div` inside the component.** Agents put styled definitions inside the function body — generates a new class on every render. Lint and reject.
- **Missing `'use client'`.** Agents drop `styled-components` into Server Components without the directive. Compile-time fail or hydration mismatch. Mandate the directive.
- **Theme typing not augmented.** Agents generate `theme.colors.primary` but skip `declare module 'styled-components' { interface DefaultTheme extends Theme {} }`. Require it in the bundle.
- **Mixing Emotion `css` prop with styled-components.** Both libs export `css`; the agent imports the wrong one and templates run as JS. Pin imports explicitly.
- **No transient prop convention.** Agents use `variant` not `$variant`; React warns about unknown DOM attribute. Force `$` prefix.
- **Theme drift between agents.** One agent uses `theme.spacing.md`, another uses `theme.space.md`; over a session the theme schema mutates. Lock the theme TS interface and use it as the contract.
- **Hardcoded hex codes in templates.** Default LLM behavior for "primary blue" is `#3b82f6` — bypasses the token system. Reject literal colors outside `theme/tokens.ts`.
- **Ignoring SSR wiring.** Agents build a styled component, ship it, and skip `ServerStyleSheet` (styled-components) or `extractCriticalToChunks` (Emotion). FOUC in production.
- **Dark mode bait-and-switch.** Agents add a `darkTheme` but no provider switch; no actual dark mode. Pair with a `<ThemeProvider>` and a hook (`useColorScheme`) — never just declare both objects.
- **Atomic CSS confusion.** Agents conflate runtime CSS-in-JS with Tailwind / Panda. `<div className={styles.btn}>` (Modules) vs `<Btn $variant="x">` (styled) vs `<div className={btn({variant:'x'})}>` (Panda) — keep one model per project.
- **Type-safety regressions on theme update.** Renaming a token requires updating the augmentation interface; agents update tokens but not the type → silent stale typings until next compile.
- **CSS reset duplication.** Agents add `createGlobalStyle` resets while a Tailwind `@base` reset already runs — double specificity wars.

## References
- styled-components docs. https://styled-components.com
- Emotion docs. https://emotion.sh
- vanilla-extract. https://vanilla-extract.style
- Linaria. https://linaria.dev
- Panda CSS. https://panda-css.com
- Compiled (Atlassian). https://compiledcssinjs.com
- React docs — Server Components & runtime CSS-in-JS. https://react.dev/reference/rsc/server-components
- Style Dictionary. https://amzn.github.io/style-dictionary/
- "A thorough analysis of CSS-in-JS." https://css-tricks.com/a-thorough-analysis-of-css-in-js/
- W3C Design Tokens Format Module. https://www.w3.org/community/design-tokens/
- Sibling methodologies in this repo: `solo/dev/frontend-developer/`, `solo/ux/ui-designer/design-tokens-fundamentals/`.
