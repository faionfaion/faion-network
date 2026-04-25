# Agent Integration — shadcn/ui Architecture

## When to use
- Mid-to-large React app already using shadcn/ui that needs a clear directory and ownership convention.
- Multiple agents/teams contribute components and you must prevent the `components/ui/` directory from becoming a junk drawer.
- Migrating away from a closed UI library and want a layered structure (primitives → composite → feature).
- Setting up a monorepo where shadcn primitives live in a shared `packages/ui/` and feature components live per-app.

## When NOT to use
- Tiny app with <20 components — flat `components/` is fine.
- Stack that is not React + Tailwind (architecture rules assume both).
- Project uses a closed UI library (MUI/Mantine) — different patterns apply.
- Pre-shadcn-init phase; start with the `shadcn-ui` methodology first, then layer architecture on.

## Where it fails / limitations
- The "primitives are vendored" rule is hard to enforce socially; agents will reach into `components/ui/` to "just fix one thing".
- Architecture rules without CI guards rot within weeks.
- Monorepo + shadcn CLI does not auto-detect package boundaries; agents need explicit `--cwd` flags.
- Themes via CSS variables work great until a feature needs a *different* theme (multi-tenant) — variable scoping has to be designed up front.
- Server vs client component boundaries leak through composition; lifting state up across the boundary often forces a rewrite.

## Agentic workflow
Treat the architecture as a contract: (1) `components/ui/*` — vendored, only mutated via `shadcn add`; (2) `components/<feature>/*` — agents author here, importing from `ui/` and `lib/utils`; (3) `lib/` — pure utilities and tokens. Add CI guards: a "shadcn primitives untouched" check, a "no cross-feature imports" check, and a "no `any` types" check. For multi-tenant theming, scope variables under `[data-theme=tenant-x]` selectors and forbid hard-coded colors in features.

### Recommended subagents
- `faion-frontend-component-agent` — feature components composed from primitives.
- `faion-storybook-agent` — stories per layer (primitive vs feature) for visual regression.
- `faion-sdd-executor-agent` — wire CI guards: pristine primitives, layering, types, a11y, bundle size.

### Prompt pattern
```
Architecture-aware prompt: "Add a CompanyBillingCard composing primitives <Card>, <Button>, <Tooltip>.
Place at components/billing/CompanyBillingCard.tsx. Import shadcn primitives from @/components/ui.
Do NOT edit primitives. Use cva() for variants if needed. Add Storybook story under same dir.
Theme via CSS variables only — no hex literals."
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `shadcn` CLI | Add primitives via `add`, diff via `diff` | `npx shadcn@latest <cmd>` |
| `class-variance-authority` | Variants in feature components | `npm i class-variance-authority` |
| `tailwind-merge` | `cn()` helper foundation | `npm i tailwind-merge` |
| `madge` | Detect cross-layer imports | `npm i -D madge` |
| `dependency-cruiser` | Enforce layering rules | `npm i -D dependency-cruiser` |
| `eslint-plugin-boundaries` | Lint layer imports | `npm i -D eslint-plugin-boundaries` |
| `size-limit` | Per-route bundle budget | `npm i -D size-limit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ui.shadcn.com | OSS docs | Yes | Source of truth for primitive code |
| TweakCN | SaaS | Yes | Theme token editor; export to `globals.css` |
| Chromatic | SaaS | Yes | Visual regression layered by primitive vs composite |
| v0.dev | SaaS | Yes | Generates shadcn-style features the agent can drop into `components/<feature>/` |
| Turborepo / Nx | OSS | Yes | Monorepo orchestration when primitives are extracted to a package |

## Templates & scripts
See `templates.md` and `examples.md`. Layering CI guard via `dependency-cruiser`:

```js
// .dependency-cruiser.cjs
module.exports = {
  forbidden: [
    {
      name: 'primitives-pure',
      severity: 'error',
      from: { path: '^components/ui' },
      to:   { path: '^components/(?!ui)' }, // primitives must not import features
    },
    {
      name: 'no-cross-feature',
      severity: 'error',
      from: { path: '^components/([^/]+)/' },
      to:   { path: '^components/(?!\\1|ui)/[^/]+/' },
    },
  ],
};
```

`cn()` helper canonical:

```ts
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
```

## Best practices
- Three layers, no more: `ui/` (primitives), `<feature>/` (compositions), `layout/` (page chrome). Resist a fourth.
- All variants use `cva()`; banned: long inline class strings, dynamic class interpolation.
- One `components.json` per app or package; in monorepos pin per-package `--cwd`.
- Theme via CSS variables only — `--background`, `--primary`, `--ring`, etc. Components consume `bg-background` etc.
- For multi-tenant: scope variables under `[data-theme="tenant-x"]` and set on `<html>`.
- Server Components by default in Next.js App Router; mark client primitives explicitly with `"use client"`.
- Treat upgrades as PRs: `npx shadcn diff` before bumping; visual regression must pass.

## AI-agent gotchas
- Agents will edit `components/ui/button.tsx` to "fix" an issue — install a CI guard or CODEOWNERS rule pinning the dir.
- LLMs forget `"use client"` on primitives that use Radix portals/state; works in dev, fails on production server build.
- Multi-tenant theming needs scoped variables; agents that hardcode `text-blue-600` defeat the design.
- `cn()` / `tailwind-merge` not imported → silent class conflicts. Lint rule: ban inline className strings >6 utilities.
- Agents tend to dump new files into `components/` flat; enforce `<feature>/` subdir convention with a path lint.
- When extracting primitives to a shared package, agents miss `peerDependencies` for React; the consumer build silently duplicates React.
- Path aliases (`@/components`, `@/lib/utils`) drift between `tsconfig`, `vite.config`, and `components.json` — keep one source.

## References
- https://ui.shadcn.com/docs
- https://github.com/sverweij/dependency-cruiser
- https://cva.style/docs
- https://tailwindcss.com/docs/dark-mode#with-css-variables
- https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns
