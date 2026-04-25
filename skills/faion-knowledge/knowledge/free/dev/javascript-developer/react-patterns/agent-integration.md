# Agent Integration — React Patterns

## When to use
- Greenfield React 18/19 app where folder layout, state-tool selection, and core component contracts must be decided upfront.
- Refactor of a React codebase that mixes class/functional, has 600+ line components, or scatters server/client/UI/form state across one global store.
- Code-review pass focused on memoization correctness, context shape, or ref-vs-state choices.
- Pre-PR audit: enforce named exports, props interfaces, and `useMemo`/`useCallback` dependency completeness.

## When NOT to use
- Non-React UI work (Vue, Svelte, Solid, plain Web Components) — patterns do not transfer literally.
- Server-only Node services (no JSX) — load `nodejs-fastify` or `nodejs-express` instead.
- Native mobile — use a React Native methodology (this README is web-shaped).
- Tiny demos / prototypes — full architecture (`features/`, `lib/`, providers) is overhead.

## Where it fails / limitations
- README does not cover Server Components / RSC streaming / `use` hook — pair with a Next.js methodology for App Router work.
- State decision tree is opinionated (TanStack Query / Zustand) — teams committed to Redux Toolkit, MobX, or XState need adaptation.
- Performance section assumes profiler-driven optimization is unavailable; agents must still verify with React DevTools profiler before adding `memo`.
- Compound-components and render-props patterns are listed in the agent-selection table but not explained in the README — agent must pull external references.

## Agentic workflow
Treat the README as the contract: layout (`components/ui`, `features/<name>`, `hooks`, `lib`), component shape (function declaration + props interface + explicit return), and state-tool mapping. A planner subagent decomposes the feature against this shape, an implementer subagent writes the files, and a reviewer subagent grep-checks for the specific anti-patterns (inline object props, missing `useCallback` deps, default exports, class components). For larger refactors, run an audit pass first that produces a file-by-file diff plan before any edit.

### Recommended subagents
- `faion-feature-executor` — sequential SDD execution; ideal for "decompose Dashboard.tsx into feature/Dashboard/*" tasks driven by the README structure.
- `faion-sdd-execution` — quality gates: enforces named exports, prop interfaces, no inline JSX styles via review checklist.
- `faion-improver` — audit-and-improve loop over an existing React tree to surface god components and missing memoization.

### Prompt pattern
```
Apply react-patterns README as the source of truth. Produce a directory plan
(features/<name>, hooks/, lib/, components/ui) for <feature>. For each file
state: file path, exported symbols, props interface, state owner (server-state
via TanStack Query, form-state via RHF, UI-state via Zustand, local via
useState). Do NOT write code yet.
```
```
Review <file> against react-patterns. Flag: (1) default exports,
(2) inline object/array literals in JSX props, (3) useEffect/useCallback with
incomplete deps, (4) Context value not wrapped in useMemo, (5) class components.
Output a numbered list with line refs only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `eslint` + `eslint-plugin-react` + `eslint-plugin-react-hooks` | Lint exhaustive-deps, no-default-export, rules of hooks | `npm i -D eslint-plugin-react-hooks` |
| `@typescript-eslint/parser` | TS-aware lint, surfaces prop-type drift | typescript-eslint.io |
| `react-scan` | Runtime render-cause inspector for memoization audits | `npm i -D react-scan` |
| `madge` | Detect circular deps and oversized barrel files in `features/` | `npx madge --circular src` |
| `ts-prune` | Find unused exports across the feature graph | `npx ts-prune` |
| `knip` | Newer alternative to ts-prune; finds unused files/exports/deps | knip.dev |
| `dpdm` | Dependency graph for `features/` boundary enforcement | `npx dpdm` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TanStack Query | OSS | Yes | Server-state of choice in README; agents drive via `useQuery`/`useMutation` keys |
| Zustand | OSS | Yes | Recommended global UI state; tiny API → predictable codegen |
| Jotai | OSS | Yes | Atom-level state; good for derived UI state |
| React Hook Form + Zod | OSS | Yes | Form state contract; schema doubles as TS types |
| Storybook | OSS | Yes | Per-component visual tests; pair with `chromatic` for visual diff in CI |
| Chromatic | SaaS | Yes (API + GH App) | Visual review for the `components/ui` primitives |
| Sentry | SaaS | Yes (CLI + sourcemaps) | Wraps `ErrorBoundary` reporting referenced by `features/` shells |

## Templates & scripts
See `templates.md` for the directory and component scaffolds. Inline helper to detect god components before refactor:

```bash
#!/usr/bin/env bash
# god-components.sh — list .tsx components over 200 lines, sorted desc
set -euo pipefail
ROOT="${1:-src}"
find "$ROOT" -name '*.tsx' ! -name '*.test.tsx' ! -name '*.stories.tsx' \
  -exec wc -l {} + \
  | awk '$1>200 && $2!="total"{print $1"\t"$2}' \
  | sort -rn | head -50
```

Also useful for hook-dep audits before edits:

```bash
npx eslint 'src/**/*.{ts,tsx}' --rule 'react-hooks/exhaustive-deps: error' --no-eslintrc --plugin react-hooks
```

## Best practices
- Co-locate `Component.tsx` + `Component.test.tsx` + `Component.styles.ts` + `index.ts`; keep barrel files single-purpose, never re-export from multiple features through one index.
- Provider value object MUST go through `useMemo` — otherwise every consumer re-renders on every parent render. Reviewer agents should grep `Context.Provider value=\{\{` as a red flag.
- Always type the context as `T | null` and throw in the consumer hook; never default to a fake object — silent bugs.
- Prefer `useReducer` once a component has 3+ related `useState` calls, especially when transitions depend on current state.
- For lists, key on stable IDs only; agents should reject `key={index}` for any list that can reorder.
- When `useCallback` is added solely "for memo", verify the consumer is `memo()`-wrapped — otherwise it is dead overhead.

## AI-agent gotchas
- LLMs love default exports; the README forbids them. Reviewer agent must hard-fail on `export default function`.
- `useEffect` dep arrays are the #1 hallucination spot — implementer agent should re-read the closure and list every referenced identifier; deferred values from refs are the only legitimate omission and require a comment.
- Server Components vs client components: an LLM will silently add `useState` to a file destined to be a Server Component. For any Next.js work, require an explicit `'use client'` decision in the plan step before code is written.
- `as const` on action constants is required for the discriminated-union state pattern; agents drop it and break narrowing.
- Inline object/array props (`style={{...}}`, `data={[...]}`) defeat `memo`; this is the most common silent perf regression — flag every instance during review.
- Human-in-loop checkpoint: after the directory plan, before any file write, when migrating a god component (loss of in-flight state and effects is high-risk).

## References
- React docs — https://react.dev/
- React TypeScript Cheatsheet — https://react-typescript-cheatsheet.netlify.app/
- TanStack Query — https://tanstack.com/query/latest
- Zustand — https://zustand-demo.pmnd.rs/
- Jotai — https://jotai.org/
- "Thinking in React" + "You Might Not Need an Effect" — react.dev/learn
