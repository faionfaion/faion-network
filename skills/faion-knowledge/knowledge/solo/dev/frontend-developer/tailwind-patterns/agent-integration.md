# Agent Integration — Tailwind Patterns

## When to use
- Existing Tailwind project that needs reusable variant patterns (button, badge, card) without a UI library.
- You want type-safe class composition via `cva()` + `cn()` for AI-generated components.
- Migrating ad-hoc utility soup into named components without giving up utility-first.
- Building a private design system on top of Tailwind for a single product.

## When NOT to use
- Project does not yet have Tailwind configured — start with the `tailwind` methodology first.
- Static marketing site that ships once and is never refactored; raw utilities are fine.
- Team prefers CSS Modules or styled-components; mixing paradigms doubles the surface area for agents.

## Where it fails / limitations
- `cva()` types get complex fast; deeply nested compoundVariants slow down `tsc` and confuse Copilot.
- `tailwind-merge` only resolves conflicts it knows about; custom plugins or arbitrary values may still collide.
- Pattern abstractions hide intent — over-extracting kills the "ctrl-F your styles" win of utility-first.
- Class-name strings inside variants are invisible to the Tailwind IntelliSense extension unless using the `tailwindCSS.experimental.classRegex` setting.
- Dynamic class strings (`bg-${color}-500`) get purged by the JIT compiler; agents that build classes by interpolation produce missing styles.

## Agentic workflow
Pattern: agent reads `templates.md` for the canonical button/input/card recipes, then proposes a `cva()` definition for any new variant. Always emit (1) the `cva()` block, (2) the `cn()`-wrapped component, (3) a story or test exercising every variant. Reject diffs that introduce raw class strings longer than ~6 utilities outside of `cva()`. Force agents to put the `tailwindCSS.experimental.classRegex` config in `.vscode/settings.json` so future agent runs see the same lint signal.

### Recommended subagents
- `faion-frontend-component-agent` — generate `cva()`-based variants per feature.
- `faion-storybook-agent` — auto-story every variant + size combination.
- `faion-sdd-executor-agent` — run `tailwind-merge` checks, ESLint Tailwind plugin, and visual regression.

### Prompt pattern
```
Build a <Badge> component using cva(). Variants: tone (info|success|warn|error), size (sm|md), withDot (bool).
Use cn(), tailwind-merge, and our color tokens (no hex). Include a Storybook story matrixing all variants.
Forbid: dynamic class interpolation, arbitrary values without // safelist comment.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` | Compile + JIT | `npm i -D tailwindcss postcss autoprefixer` |
| `class-variance-authority` | Variant API | `npm i class-variance-authority` |
| `tailwind-merge` | Conflict resolution | `npm i tailwind-merge` |
| `clsx` | Conditional class strings | `npm i clsx` |
| `eslint-plugin-tailwindcss` | Lint class order, deprecated classes, conflicts | `npm i -D eslint-plugin-tailwindcss` |
| `prettier-plugin-tailwindcss` | Auto-sort classes | `npm i -D prettier-plugin-tailwindcss` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind UI | SaaS | Yes (snippet copy) | Premium component patterns, agent can consume HTML |
| Tailwind Play | SaaS | Yes (URL-based) | Share reproducible playgrounds for agents |
| TweakCN | SaaS | Yes | Token editor that exports tailwind config |
| Chromatic | SaaS | Yes | Visual regression for variant matrices |

## Templates & scripts
See `templates.md` for full button/input recipes. Minimal `cn()` helper (canonical):

```ts
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Pattern lint to catch dynamic class interpolation (Tailwind purges those):

```bash
# scripts/check-no-interp-classes.sh
set -euo pipefail
if git grep -nE 'className=\{?`[^`]*\$\{[^}]+\}[^`]*`' -- 'src/**/*.tsx' 'src/**/*.ts'; then
  echo "Dynamic Tailwind class interpolation detected (will be purged by JIT)."
  exit 1
fi
```

## Best practices
- One `cva()` per component, kept next to the component file; do not centralize across the app.
- Variants describe **intent** (`tone="danger"`), not **style** (`color="red"`). Tone maps to tokens.
- Use `compoundVariants` for "this combo needs an override", not for new variants.
- Add a Storybook story per variant matrix; visual regression catches token drift.
- Use `data-*` attributes (`data-state`, `data-loading`) and Tailwind's `data-[state=open]:` selector instead of toggling class strings imperatively.
- Safelist arbitrary or dynamic classes explicitly in `tailwind.config.ts` `safelist`.

## AI-agent gotchas
- Agents love string templates (`bg-${variant}-500`) — these are JIT-purged. Use lookup objects with full class strings.
- `tailwind-merge` does not know about your custom plugins; agents that ship a new plugin must update the `extendTailwindMerge` config.
- LLMs sometimes propose `@apply` chains in a global stylesheet; this defeats the per-component variant pattern. Reject in code review.
- ESLint plugin "classnames-order" autofix can reorder cva() variant strings unpredictably; pin rule severity to `warn` in cva files.
- When agents add new colors to `tailwind.config`, they often forget the matching CSS variable in `globals.css`; the build "works" but dark mode looks broken.

## References
- https://cva.style/docs
- https://github.com/dcastil/tailwind-merge
- https://tailwindcss.com/docs/reusing-styles
- https://github.com/francoismassart/eslint-plugin-tailwindcss
