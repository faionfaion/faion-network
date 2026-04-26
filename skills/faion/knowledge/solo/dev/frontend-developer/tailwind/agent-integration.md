# Agent Integration — Tailwind CSS

## When to use
- Greenfield app or rewrite where you control HTML and want utility-first styling.
- Multi-developer / multi-agent project: utilities give a stable, gre­pable styling surface.
- You need fast iteration on visual design, with token control via config.
- Pairing with React/Vue/Svelte/HTMX where templating already lives near markup.

## When NOT to use
- Brownfield app with mature CSS-in-JS or BEM conventions; mixing causes specificity wars.
- Email templates, PDFs, or print-first surfaces (Tailwind's reset and JIT do not cleanly target those).
- Library/SDK that ships CSS — utility classes leak global resets onto consumer apps.
- Strict design system that bans "magic numbers" — utilities make ad-hoc spacing too easy.

## Where it fails / limitations
- Long class strings hurt readability; without `cva()` or component extraction, diffs become noise.
- JIT compiler scans content globs only; classes built outside those globs (markdown, CMS, JSON) are purged.
- Tailwind v3 → v4 changed config (CSS-first config, `@theme` block); training data straddles both, agents conflate them.
- Plugin ecosystem (typography, forms, container queries) requires explicit registration; agents often forget.
- Server-side templating engines (Django, Rails) need `content` glob updates; new templates render unstyled until config bumped.

## Agentic workflow
Bootstrap once with `tailwindcss init -p` (v3) or `@tailwindcss/cli init` (v4), commit `tailwind.config.ts`, `postcss.config.js`, and `globals.css`. Agents thereafter only edit components and the theme block. Treat `tailwind.config.ts` as a token contract: any change goes through a token-update PR. Pair with `tailwind-patterns` methodology for variant abstractions (cva). For framework integration, prefer official plugins (`@tailwindcss/vite`, `@tailwindcss/postcss`) over hand-rolled PostCSS chains.

### Recommended subagents
- `faion-sdd-executor-agent` — bootstrap config, install plugins, wire CI lint.
- `faion-frontend-component-agent` — author components with utility classes + `cn()`.
- `faion-storybook-agent` — render token swatches and component states for visual regression.

### Prompt pattern
```
Initialize Tailwind in this Vite + React + TS project. Use Tailwind v4 with CSS-first config.
Deliver: tailwind.config.ts (or @theme block), src/styles/globals.css, postcss.config (if needed).
Add tokens for brand.{50..900} (HSL triplets) and font.sans=Inter. Wire prettier-plugin-tailwindcss.
Do not edit any component files in this task.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` v3 | JIT compile, init scaffolding | `npx tailwindcss init -p` |
| `@tailwindcss/cli` v4 | New CLI, CSS-first config | `npm i -D tailwindcss @tailwindcss/cli` |
| `@tailwindcss/vite` | Vite integration (v4) | `npm i -D @tailwindcss/vite` |
| `@tailwindcss/postcss` | PostCSS plugin | `npm i -D @tailwindcss/postcss` |
| `@tailwindcss/typography` | Prose styling | `npm i -D @tailwindcss/typography` |
| `@tailwindcss/forms` | Form reset | `npm i -D @tailwindcss/forms` |
| `prettier-plugin-tailwindcss` | Auto class sort | `npm i -D prettier-plugin-tailwindcss` |
| `eslint-plugin-tailwindcss` | Class lint | `npm i -D eslint-plugin-tailwindcss` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind Play | SaaS | Yes | Reproducible playgrounds via URL |
| Tailwind UI | SaaS | Yes | Paid component snippets; deterministic copy |
| Headless UI | OSS | Yes | Behavior primitives by Tailwind Labs |
| TweakCN | SaaS | Yes | Visual token editor → config export |
| Tailwind Variants | OSS | Yes | Alternative to cva(), nicer slot API |

## Templates & scripts
See `templates.md`. Minimal v4 setup:

```css
/* src/styles/globals.css */
@import "tailwindcss";

@theme {
  --color-brand-50: hsl(214 100% 97%);
  --color-brand-500: hsl(217 91% 60%);
  --color-brand-900: hsl(224 64% 33%);
  --font-sans: "Inter", system-ui, sans-serif;
  --radius-md: 0.5rem;
}
```

Class-order CI guard:

```bash
# scripts/check-class-order.sh
set -euo pipefail
npx prettier --check 'src/**/*.{ts,tsx,jsx,html}' --plugin prettier-plugin-tailwindcss
npx eslint 'src/**/*.{ts,tsx}' --rule 'tailwindcss/classnames-order: error'
```

## Best practices
- Configure `content` glob explicitly; do not rely on autodetection. Include MDX, Markdown, server templates.
- Theme via design tokens (CSS variables in v4 `@theme`, `theme.extend` in v3). No hardcoded hex in components.
- Use `prettier-plugin-tailwindcss` to canonicalize class order across all agent outputs.
- Avoid `@apply` except for thin component wrappers (e.g. `.prose-fix`); abstractions belong in components.
- Adopt mobile-first: write base classes for mobile, prefix with `sm:`/`md:` to scale up.
- Use `data-*` selectors (`data-[state=open]:opacity-100`) instead of toggling classes imperatively.

## AI-agent gotchas
- v3 vs v4 config format: agents fed mixed examples produce a `tailwind.config.ts` that v4 silently ignores. Specify the major version in the prompt.
- Auto-purge depends on string-literal scanning. Agents that build class names with template literals or `clsx` arrays of conditional fragments must keep all candidates as full literal strings.
- When agents install `@tailwindcss/forms`, they often forget `strategy: 'class'`, breaking existing custom inputs.
- Dark mode strategy (`media` vs `class`) is a one-line config; agents flipping it without checking existing components produce contrast bugs.
- LLMs love `@apply` chains; treat as a smell. Reject in PRs unless the file is `globals.css` and chain is ≤3 utilities.
- After installing a plugin, agents forget to add it to `plugins:` in v3 config. CI typecheck passes, runtime styles silently missing.

## References
- https://tailwindcss.com/docs
- https://tailwindcss.com/blog/tailwindcss-v4 (CSS-first config)
- https://headlessui.com/
- https://tailwind-variants.org/
- https://github.com/tailwindlabs/prettier-plugin-tailwindcss
