# Agent Integration — CSS-in-JS Advanced

## When to use
- Migrating a styled-components / Emotion codebase to a zero-runtime solution (vanilla-extract, Linaria, Panda CSS, StyleX) for Core Web Vitals or React Server Components.
- Building a typed atomic CSS layer (Sprinkles / Panda recipes) when Tailwind doesn't fit (e.g., heavy theming, multi-brand white-label).
- Setting up SSR style extraction for a styled-components / Emotion app on Next.js Pages Router or Remix.
- Optimizing a runtime CSS-in-JS app whose Largest Contentful Paint is dominated by serialized CSS injection.

## When NOT to use
- New apps where Tailwind + CSS variables solves the problem — runtime CSS-in-JS adds bundle and hydration cost without theming gains.
- React Server Components-only trees: styled-components and Emotion runtime require a `'use client'` boundary; pick `vanilla-extract`, Panda, or StyleX instead.
- Component libraries published to npm — runtime CSS-in-JS forces the consumer's bundler to ship the runtime; ship plain CSS or zero-runtime output.

## Where it fails / limitations
- styled-components v6 + Next.js App Router needs `styled-components/registry` and `compiler.styledComponents = true`; agents routinely produce hydration-mismatch warnings without it.
- vanilla-extract's `.css.ts` files run in a Node sandbox at build time — `process.env`, `window`, and dynamic imports break the build cryptically.
- Sprinkles bundles every variant combo as static classnames; over-broad `properties` arrays explode CSS size by 5-10x.
- Emotion `css` prop with TS strict mode requires `/** @jsxImportSource @emotion/react */` per file or it silently degrades to plain `style`.

## Agentic workflow
Drive vanilla-extract / Panda / StyleX migrations with subagents that (1) inventory existing styled components, (2) translate them file-by-file, (3) run typecheck + Storybook visual diff after every batch, (4) commit per-batch. Keep the human in the loop for theming decisions (CSS variables vs themes API) — those become load-bearing later. For SSR style extraction, the agent should produce the registry/document changes and a Playwright assertion that no FOUC occurs on first paint.

### Recommended subagents
- `faion-feature-executor` — sequential per-component migration with a "build + visual-test" quality gate between commits.
- `faion-sdd-executor-agent` — full SDD loop when the migration is large enough to warrant a spec + design + tasks.

### Prompt pattern
- "Convert `src/components/Button.tsx` from styled-components to vanilla-extract recipes. Preserve prop API. Output `Button.css.ts` and updated `Button.tsx`. Then write a story that exercises every variant."
- "Find all `styled.X` calls inside render bodies in `src/`. Return a refactor plan that lifts them to module scope and threads dynamic values via `$prefix` transient props or CSS variables."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm add @vanilla-extract/{css,recipes,sprinkles}` | Zero-runtime CSS-in-TS | https://vanilla-extract.style |
| `pnpm add -D @vanilla-extract/vite-plugin` (or webpack/next plugin) | Build-time extraction | https://vanilla-extract.style/documentation/integrations/vite/ |
| `pnpm add @pandacss/dev && panda init` | Panda CSS — runtime-free, CSS-variable-based | https://panda-css.com |
| `pnpm add @stylexjs/stylex` | Meta StyleX — atomic, deterministic, RSC-safe | https://stylexjs.com |
| `pnpm add styled-components` (v6+) | Runtime CSS-in-JS, RSC requires registry | https://styled-components.com |
| `npx @emotion/eslint-plugin` | Lint Emotion-specific anti-patterns | https://emotion.sh/docs/@emotion/eslint-plugin |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | Yes | Catches visual regressions during migration; treat as oracle for "did the styles actually change?". |
| Bundlephobia | SaaS (web) | Partial | Use to compare runtime cost; no API for agents — wrap with `npm-bundle-size`. |
| Statoscope / Webpack Bundle Analyzer | OSS | Yes | Agents can parse JSON output to verify CSS extraction worked. |
| Linaria | OSS | Yes | Alternative zero-runtime; tagged-template syntax is closer to styled-components for migration. |

## Templates & scripts
See `templates.md` for vanilla-extract recipe and Sprinkles boilerplate. Migration audit script:

```bash
#!/usr/bin/env bash
# scripts/find-runtime-styled-in-render.sh
# Flag styled.X calls defined inside React components (perf footgun)
set -euo pipefail
grep -rEn "function [A-Z][a-zA-Z]*\\(.*\\) \\{" src --include='*.tsx' -A 50 \
  | grep -E "(const|let) [A-Z][a-zA-Z]* = styled\\." \
  || echo "OK: no styled components defined inside render"
```

## Best practices
- Pick exactly one CSS-in-JS library per app. Mixing `styled-components` + `Emotion` doubles runtime and breaks themes.
- Keep `*.css.ts` files dependency-free of app code — only import other `*.css.ts`, types, and constants. Anything else slows the build sandbox.
- Use CSS variables for any value that changes per render (theme, animation target). Avoid prop-driven `styled.div` for hot paths — set the variable via inline `style`.
- For SSR with styled-components, always render through the registry and write a Playwright test that asserts `<style data-styled>` appears in the initial HTML.
- Treat Sprinkles `properties` like a public API: every added property compiles to N classnames. Audit the generated CSS size in CI.

## AI-agent gotchas
- Agents copy `RecipeVariants<typeof button>` but forget the matching `defaultVariants`; output throws at runtime because the recipe receives `undefined`.
- LLMs often write `vars: { color: '#3b82f6' }` instead of using `createVar()` + `assignVars`, breaking theme switching.
- For Emotion in App Router, generated code omits `'use client'` and the `CacheProvider`; FOUC + hydration mismatch.
- Agents reach for `&& css\`...\`` template-string composition and lose TS types — prefer recipe variants over prop-conditional template strings.
- When asked to "make it faster", agents memoize the wrong layer (memoizing `css` calls instead of lifting styled components out of render).

## References
- vanilla-extract — https://vanilla-extract.style/
- Panda CSS — https://panda-css.com
- StyleX — https://stylexjs.com
- styled-components SSR — https://styled-components.com/docs/advanced#server-side-rendering
- Emotion SSR — https://emotion.sh/docs/ssr
- Josh Comeau, "The Styled-Components Happy Path" — https://www.joshwcomeau.com/css/styled-components/
