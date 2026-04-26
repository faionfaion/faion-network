# Agent Integration — React Hooks

## When to use
- Writing or reviewing functional components and custom hooks in React 18/19.
- Extracting reusable logic out of god components into named `use*` hooks.
- Fixing render bugs that show up as stale closures, infinite loops, or broken cleanup.
- Adding strict-mode-safe data fetching with abort and cancellation.
- Audit pass for memoization correctness (`useCallback`/`useMemo` dep arrays).

## When NOT to use
- Class components or legacy lifecycle code — different rules; migrate first.
- Server Components / RSC — most hooks are client-only; need the `'use client'` boundary or a Next.js methodology.
- Unrelated frameworks (Vue, Svelte) — primitives differ, naming doesn't transfer.
- React Native lifecycle work that depends on platform listeners not covered here.

## Where it fails / limitations
- README does not cover React 19's `use`, `useActionState`, `useFormStatus`, `useOptimistic`, or the new `ref` callback contract — pair with `typescript-react-2026` or React 19 release notes.
- Memoization advice predates the React Compiler (RC) era; with the compiler enabled, manual `useMemo`/`useCallback` are often redundant. Verify whether the project enables the compiler before insisting on manual memoization.
- `useEffect` data-fetch examples don't replace TanStack Query — for non-trivial server state, prefer that.
- `useReducer` and `useSyncExternalStore` get short coverage; agents must consult external docs for stores and concurrent reads.

## Agentic workflow
Two phases. Audit phase: a reviewer subagent reads the file, lists every hook call site, and emits a table of (hook, deps, captured identifiers, missing deps, cleanup correctness). Fix phase: implementer subagent applies the minimal change — usually completing the dep array, hoisting a callback into a stable ref, or splitting the effect into two. Reviewer verifies that no `useEffect` fires per-render due to inline object/array deps.

### Recommended subagents
- `faion-feature-executor` — sequential extraction tasks (one component → one hook per task) with `vitest run` gate.
- `faion-sdd-execution` — pattern memory for canonical hooks (`useDebounce`, `useLocalStorage`, `useFetchWithAbort`).
- `faion-improver` — periodic audit producing a "memoization debt" list with file:line refs.

### Prompt pattern
```
Audit hooks in <file>. For each hook, output:
hook | deps | identifiers actually used | missing deps | cleanup OK? | notes.
Do not modify code.
```
```
Extract <logic block> into a custom hook named use<Thing>. Contract: input
typed, return is an object literal. Keep cleanup, abort, and dep arrays
faithful. Update call sites. Run `vitest run` and `tsc --noEmit`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `eslint-plugin-react-hooks` | `rules-of-hooks` + `exhaustive-deps` | `npm i -D eslint-plugin-react-hooks` |
| `eslint-plugin-react-compiler` (RC) | Validates components compile-friendly | react.dev/learn/react-compiler |
| `react-scan` | Runtime view of which hooks/components re-render | `npm i -D react-scan` |
| `@testing-library/react` + `renderHook` | Unit tests for custom hooks | testing-library.com |
| `why-did-you-render` | Pinpoint avoidable re-renders | `npm i -D @welldone-software/why-did-you-render` |
| React DevTools Profiler | Manual profiling before adding `memo` | react.dev/learn/react-developer-tools |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TanStack Query | OSS | Yes | Replaces hand-rolled `useEffect` fetch in 80% of cases |
| SWR | OSS | Yes | Lighter alternative to TanStack Query |
| use-debounce | OSS | Yes | Battle-tested debounce hook; agents stop reinventing |
| usehooks-ts (OSS) | OSS | Yes | Library of typed primitive hooks; good base for `useLocalStorage` etc. |
| Sentry | SaaS | Yes | Captures errors thrown inside effects; pair with React ErrorBoundary |

## Templates & scripts
See `templates.md` for `useFetchWithAbort`, `useDebounce`, `useLocalStorage`. Inline scanner for missing-dep risks before review:

```bash
#!/usr/bin/env bash
# hook-audit.sh — list useEffect/useCallback/useMemo with deps array on next line for grep review
set -euo pipefail
ROOT="${1:-src}"
grep -RnE 'use(Effect|Callback|Memo|LayoutEffect)\(' "$ROOT" \
  --include='*.ts' --include='*.tsx' \
  -A 6 \
  | sed -n '1,200p'
```

ESLint focused run (no project config needed):

```bash
npx eslint 'src/**/*.{ts,tsx}' --no-eslintrc \
  --plugin react-hooks --rule '{"react-hooks/exhaustive-deps":"error","react-hooks/rules-of-hooks":"error"}' \
  --parser-options=ecmaVersion:latest,sourceType:module,ecmaFeatures:{jsx:true}
```

## Best practices
- Custom hooks return either a tuple (state, setter) for primitives or a named object for richer APIs — never a plain array of unrelated values.
- Always provide cleanup in `useEffect` for: subscriptions, timers, event listeners, AbortControllers. Reviewer must reject any subscription without a return.
- For "callback that should always reflect latest props but not change identity", use the ref-pattern (assign to `ref.current` in render, read in event handler) — it's the only acceptable way to avoid changing dep arrays.
- Never write `useEffect` to derive state from props — derive in render or via `useMemo`.
- `useCallback`/`useMemo` only earn their cost when the consumer is `memo`-wrapped or the dep is itself a stable identity feeding another memoization. Profile before adding.
- For external mutable stores, prefer `useSyncExternalStore` over hand-rolled subscriptions in `useEffect`.

## AI-agent gotchas
- LLMs frequently omit one identifier in the dep array (especially derived constants from props). Reviewer must enumerate every captured identifier line by line.
- They also wrap things in `useCallback` reflexively even when there's no `memo` consumer — pure overhead. Reject without a stated reason.
- Async functions passed directly to `useEffect` are forbidden; agents do this often. Pattern: declare async fn inside, call it, return cleanup.
- `useState(initial)` with a non-trivial expression evaluates every render unless wrapped in a thunk: `useState(() => compute())`. Agents skip the thunk silently.
- React 19's auto-memoization may make manual memoization a regression. Check for `babel-plugin-react-compiler` or the eslint plugin before recommending more `useMemo`.
- Human-in-loop checkpoint: when refactoring an effect that has timing semantics (subscriptions to mutable stores, animation frames). Easy to break in subtle ways.

## References
- React Hooks reference — https://react.dev/reference/react/hooks
- "You Might Not Need an Effect" — https://react.dev/learn/you-might-not-need-an-effect
- React Compiler — https://react.dev/learn/react-compiler
- TanStack Query — https://tanstack.com/query/latest
- usehooks-ts — https://usehooks-ts.com/
- testing-library — https://testing-library.com/docs/react-testing-library/api/#renderhook
