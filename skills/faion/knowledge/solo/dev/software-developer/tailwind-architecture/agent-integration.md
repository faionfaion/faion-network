# Agent Integration — Tailwind Architecture

## When to use
- Greenfield React/Vue/Svelte/Next.js apps where utility-first is the team standard
- Building / maintaining design-token-driven Tailwind config for a multi-app design system
- Refactoring CSS Modules / styled-components / SCSS layers to Tailwind v3 / v4
- Auditing utility class chaos in an existing Tailwind codebase (extracting components, normalizing variants)
- Wiring `tailwind-merge` + `cva` / `tv()` patterns for variant-rich component libraries (shadcn/ui style)

## When NOT to use
- Email HTML (CSS support sparse — use inlining tools, not Tailwind)
- Heavily customized print stylesheets where atomic utilities fight pagination rules
- Strict CSP environments banning `style-src 'unsafe-inline'` for Tailwind's runtime — only matters if you use Twind/JIT-in-browser
- Static-site generators with a hard 14KB CSS budget where utility CSS exceeds the limit
- Server-rendered apps that ship full markup to non-Tailwind designers maintaining handcrafted CSS

## Where it fails / limitations
- Tailwind v4 alpha config (`@theme` in CSS, no `tailwind.config.js`) is a breaking change; agents trained on v3 emit v3 config files into v4 projects and break the build
- `@apply` is a footgun at scale — agents reach for it from training-era examples; current guidance: extract a React/Vue component instead
- Class purging fails with dynamic class names (`bg-${color}-500`) — agent must safelist or refactor to a static lookup map
- `tailwind-merge` doesn't know custom design-token utilities until configured; conflicting classes silently both apply
- `prettier-plugin-tailwindcss` reorders inside template strings; agents emitting `clsx` arguments may lose intended order
- Specificity wars with global CSS / shadcn `:is()` selectors — utility wins inconsistently across browsers
- IDE class-name suggestions get stale when `theme.extend` changes; agents propose nonexistent classes

## Agentic workflow
Treat Tailwind config as a typed contract: agent edits design tokens (in `tailwind.config.{ts,js}` or v4 `@theme` block), runs the type-checked codegen for `cva`/`tv`, then a review subagent runs `eslint-plugin-tailwindcss` + `prettier-plugin-tailwindcss` and fails on unknown utilities. Component extraction policy: any duplicated 5+ utility chain across 3+ files becomes a primitive component with `cva` variants.

### Recommended subagents
- General-purpose subagent — utility refactors, variant extraction
- `faion-feature-executor` — pipeline: edit tokens → codegen → migrate consumers → assert visual regression
- `faion-sdd-execution` — gate enforcing `eslint-plugin-tailwindcss` clean + no `@apply` outside `@layer components`
- Visual-regression subagent (Playwright + Percy/Chromatic) — diff before/after refactor

### Prompt pattern
```
Migrate the Card component to a `cva` variant API.
1. Identify all <Card>/<div className="card-..."> sites with grep.
2. Define base + variants (size: sm/md/lg, intent: default/elevated/outline) in cva.
3. Replace usages, preserving className passthrough via cn(...).
4. Run `pnpm lint && pnpm test` and `playwright test --project=visual`.
Output: a diff plus a coverage table (sites migrated / total).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` CLI | Build / watch / JIT compile | `npm i -D tailwindcss postcss autoprefixer` |
| `prettier-plugin-tailwindcss` | Auto-sort utility order | `npm i -D prettier-plugin-tailwindcss` |
| `eslint-plugin-tailwindcss` | Lint unknown / shorthand-able classes | `npm i -D eslint-plugin-tailwindcss` |
| `tailwind-merge` | Resolve class conflicts at runtime | `npm i tailwind-merge` |
| `class-variance-authority` (`cva`) | Variant API | `npm i class-variance-authority` |
| `tailwind-variants` (`tv`) | Variant API w/ slot support + tw-merge | `npm i tailwind-variants` |
| `clsx` | Conditional class joining | `npm i clsx` |
| `@tailwindcss/forms`, `@tailwindcss/typography`, `@tailwindcss/aspect-ratio` | Official plugins | `npm i -D ...` |
| `headlessui` / `radix-ui` | Unstyled accessible primitives paired with Tailwind | `npm i @radix-ui/react-*` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind UI | SaaS (paid) | Read-only | Reference patterns; agents copy markup verbatim |
| shadcn/ui | OSS (CLI-installed) | Yes | `npx shadcn-ui add button` — agents drive component scaffolding |
| Catalyst | SaaS | No | Closed source; reference only |
| Storybook + Chromatic | SaaS / OSS | Yes | Visual snapshots gating Tailwind refactors |
| Percy / Loki | SaaS / OSS | Yes | Visual regression CI |
| Style Dictionary | OSS | Yes | Generate Tailwind theme from design tokens |
| Figma Tokens / Tokens Studio | SaaS / Figma plugin | Partial | Export → Style Dictionary → Tailwind theme pipeline |

## Templates & scripts
See `templates.md` for full `cn()` helper, `cva` variant patterns, and design-token-driven `tailwind.config.ts`. Minimal v3 config consuming Style Dictionary tokens:

```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss';
import tokens from './tokens/dist/js/tokens.js';

export default {
  content: ['./src/**/*.{ts,tsx,mdx}'],
  theme: {
    extend: {
      colors: tokens.color,         // semantic + primitive
      spacing: tokens.spacing,
      fontFamily: tokens.font.family,
      borderRadius: tokens.radius,
      boxShadow: tokens.shadow,
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
} satisfies Config;
```

## Best practices
- Configure `tailwind-merge` once, export your project-tuned `cn()` (handles custom token utilities) and ban raw `clsx`-only joins in lint
- Use `cva` (or `tv()` for slot-heavy components) for any component with >2 visual variants — kills branching ternary chains
- Keep `@apply` out of component code; allowed only inside `@layer components` for true CSS-only primitives (e.g., `.prose` overrides)
- Lock Tailwind version + plugin versions in lockfile; minor versions add utilities the IDE will autocomplete then break in CI
- Theming (light/dark/brand variants) via CSS custom properties referenced in `tailwind.config`, not separate compiled themes
- Set `safelist` for any class generated dynamically (e.g., `bg-${tone}`) or refactor to lookup map — never trust JIT to find them
- Co-locate Storybook stories with components; visual snapshots become the regression contract for utility refactors
- v4 migration: pre-pin `tailwindcss@^3.4`, then upgrade with explicit codemod (`npx @tailwindcss/upgrade`) — never let the agent drift to v4 mid-feature

## AI-agent gotchas
- LLMs frequently emit deprecated `bg-opacity-*` instead of `bg-black/50` slash syntax — modern Tailwind has had `/` for years; lint must catch
- Agents output `className={`...${dynamic}...`}` template strings that JIT cannot purge → unstyled production. Force lookup tables.
- `tailwind-merge` config drift: agents add custom utilities to `theme.extend` but forget the `extendTailwindMerge` call; result: conflicts silently both apply
- v3 vs v4 config syntax mixing — verify the file extension and surrounding imports before generating config
- `prettier-plugin-tailwindcss` rewrites class order on save; agents diffing pre/post format see noise — always run formatter before review
- Agents over-extract components for 2-utility duplicates ("ButtonRow"); the cost of indirection > duplication. Set a 5-utility / 3-site threshold.
- Human-in-loop checkpoint when: changing primary brand color, adding global font, modifying `screens` breakpoints — these reflow every component
- Do not paste compiled CSS output into LLM context; always feed the `tailwind.config` + a few representative components

## References
- Tailwind CSS docs: https://tailwindcss.com/docs
- Refactoring UI book (Wathan/Schoger) — utility-first principles
- shadcn/ui: https://ui.shadcn.com/
- `cva` docs: https://cva.style/
- `tailwind-variants` docs: https://www.tailwind-variants.org/
- `tailwind-merge` README: https://github.com/dcastil/tailwind-merge
- `eslint-plugin-tailwindcss`: https://github.com/francoismassart/eslint-plugin-tailwindcss
- Tailwind v4 alpha announcement: https://tailwindcss.com/blog/tailwindcss-v4-alpha
