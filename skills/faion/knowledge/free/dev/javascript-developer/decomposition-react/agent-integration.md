# Agent Integration — React Decomposition

## When to use
- Refactoring god components (>200 lines, 10+ hooks, mixed API/UI/state) into the README's feature-folder layout.
- Greenfield React/Next.js where the agent must commit to a directory shape early so subsequent feature work fits a predictable mold.
- LLM-friendly grooming: reducing per-file token counts so future agents can read whole files inside one tool call.
- Migrating from "components/" flat layout to feature-based modules with co-located hooks, types, services, stores.

## When NOT to use
- Tiny apps (<20 components) — feature/services/stores split is overhead.
- One-shot prototypes / spikes — premature decomposition is more lines for less value.
- Codebases dominated by Server Components — file-size reasoning differs; `.server.tsx` boundaries override the layout.
- UI-only design-system repos (Storybook component libraries) — they need a different shape (`packages/ui/<Component>`).

## Where it fails / limitations
- The "30-80 lines per file" target is a heuristic, not a constraint — long but cohesive components (forms with many fields) are fine and shouldn't be split for cosmetic reasons.
- Decomposition adds prop-drilling unless paired with state-tool choices (TanStack Query, Zustand) — agents must propose state ownership in the same plan.
- The layout assumes a single app; monorepo (turborepo/nx) projects need an outer shell (`apps/<name>/src/...`).
- Re-export barrels (`index.ts`) make tree-shaking analysis harder; some toolchains penalize them.

## Agentic workflow
Always plan before edit. A planner subagent produces the target tree (paths, sizes, exports, hook ownership) and a "moves table" (old path → new path → renames). An implementer subagent executes one file move per task with `git mv` to preserve history. A reviewer subagent verifies that no file regrows past 80 lines and that imports use feature-relative paths, not deep cross-feature reaches.

### Recommended subagents
- `faion-feature-executor` — sequential moves with `tsc --noEmit` + `vitest run` after each task; rolls back on type breakage.
- `faion-sdd-execution` — pattern memory for naming (e.g., `useDashboardData`, `dashboardApi`) so consistency carries across features.
- `faion-improver` — periodic audit producing god-component list and proposing splits.

### Prompt pattern
```
Apply decomposition-react to <feature path>. Output: target tree (file paths
and ~line counts), moves table (old → new), state owners (server vs UI vs
form), public exports per index.ts. Do NOT write code yet.
```
```
Execute moves table for <feature> using `git mv`. After each move run
`tsc --noEmit`. If a file exceeds 100 lines after the split, propose a sub-split
in the same task. Stop on first type error and report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git mv` | Preserves blame across file moves | git-scm.com |
| `madge` | Visualize dependency graph; spot cross-feature deep imports | `npx madge src` |
| `dpdm` | Dependency analyzer with circular-dep detection | `npx dpdm` |
| `knip` | Find unused exports/files after decomposition | knip.dev |
| `ts-prune` | Older alternative to knip | `npx ts-prune` |
| `eslint-plugin-boundaries` | Enforce that `features/a` does not import `features/b/*` | github.com/javierbrea/eslint-plugin-boundaries |
| `wc -l`, `find` | Quick size audit (see inline below) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | Yes | Per-feature stories live next to the component file; co-location story scales |
| Chromatic | SaaS | Yes | Visual regression for the new `components/ui` primitives |
| Sentry | SaaS | Yes | Per-feature error boundaries; tag events with `feature.name` |
| TanStack Query | OSS | Yes | Hosts server-state for each feature; per-feature query keys prevent leaks |
| Zustand | OSS | Yes | Slice-per-feature pattern aligns with the layout |
| Nx / Turborepo | OSS | Yes | If the app outgrows one package, features → packages translates cleanly |

## Templates & scripts
See `templates.md` for the canonical `features/<name>/` skeleton. Inline god-component scan to feed the planner:

```bash
#!/usr/bin/env bash
# god-scan.sh — top oversized .tsx files for decomposition planning
set -euo pipefail
ROOT="${1:-src}"
{
  printf "LINES\tFILE\n"
  find "$ROOT" -name '*.tsx' \
    ! -name '*.test.tsx' ! -name '*.stories.tsx' ! -name '*.types.tsx' \
    -exec wc -l {} + \
    | awk '$2!="total" && $1>120 {print $1"\t"$2}' \
    | sort -rn
} | head -40
```

Boundary lint snippet to prevent cross-feature deep imports:

```js
// eslint.config.js (excerpt)
import boundaries from 'eslint-plugin-boundaries';
export default [{
  plugins: { boundaries },
  settings: { 'boundaries/elements': [
    { type: 'feature', pattern: 'src/features/*' },
    { type: 'shared',  pattern: 'src/{components,hooks,lib,utils,types}/*' },
  ]},
  rules: { 'boundaries/element-types': ['error', { default: 'disallow', rules: [
    { from: 'feature', allow: ['shared'] },
    { from: 'shared',  allow: ['shared'] },
  ]}]},
}];
```

## Best practices
- Co-locate `Component.tsx` + `Component.test.tsx` + `Component.stories.tsx` + `Component.types.ts` + optional `Component.styles.ts`. One folder per public component.
- A feature folder owns its hooks, services thin-wrappers, types, and stores. Cross-feature reuse → promote to `src/components/ui` or `src/lib`, never deep-import.
- Public surface of a feature is `features/<name>/index.ts`. Anything not in that barrel is internal.
- Don't split for cosmetics: a 90-line cohesive form is more readable than five 20-line files.
- Hooks belong in `features/<name>/hooks/` if feature-specific, in `src/hooks/` if reused across two or more features.
- Generated code (OpenAPI clients, codegen) goes under `src/lib/<source>/` and is excluded from the line-count audit.

## AI-agent gotchas
- Agents over-split: a `Button` becomes `Button.tsx` + `Button.handlers.ts` + `Button.constants.ts` for a 40-line component. Reviewer must merge.
- Barrel files (`index.ts`) accumulate stale re-exports; agents add but never remove. Run `knip` after each refactor pass.
- Cross-feature imports leak in via auto-imports (VS Code, Cursor) — pinned tsconfig `paths` plus `eslint-plugin-boundaries` is the only durable fix.
- During moves, agents forget to update `vitest`/`storybook` configs or `tsconfig.paths`. Always re-run `tsc --noEmit` and `vitest run` after a batch of moves.
- React Server / Client split is invisible to layout — moving a `useState` component into a Server Component file silently breaks. Plan must mark each file as server/client.
- Human-in-loop checkpoint: the moves-table review. Once approved, executor can run unattended; before approval, do not move files.

## References
- "Bulletproof React" project structure — https://github.com/alan2207/bulletproof-react
- Kent C. Dodds on collocation — https://kentcdodds.com/blog/colocation
- React docs on file structure — https://react.dev/learn/thinking-in-react
- eslint-plugin-boundaries — https://github.com/javierbrea/eslint-plugin-boundaries
- knip — https://knip.dev/
