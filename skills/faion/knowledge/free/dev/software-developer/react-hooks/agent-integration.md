# Agent Integration — React Hooks Best Practices

Methodology covers Rules of Hooks, useState/useEffect/useMemo/useCallback patterns, custom hooks, cleanup. Use this file as the playbook for Claude subagents producing or auditing React functional components.

## When to use
- New functional components needing state, effects, refs, context.
- Refactor of class components to functional + hooks.
- Extracting reused logic into custom hooks (`useFoo`).
- Performance audit: unnecessary re-renders, stale closures, memo bloat.
- Migrating from older patterns (`componentDidMount` lifecycle in functional shims) to current React 18+ idioms.

## When NOT to use
- React Server Components (RSC) — most hooks are client-only; `'use client'` boundary required, server components cannot use state/effects.
- Pre-React 16.8 codebases — hooks unavailable; refactor to upgrade React first.
- Heavy state management (cross-page state machines, optimistic updates with conflict resolution) — Zustand / Redux Toolkit / TanStack Query handle better than raw `useReducer`.
- Visual / pure presentational components — adding `useCallback`/`useMemo` without measuring is premature.
- Components that should be Server Actions (form submits) in Next.js App Router — use `'use server'` actions; hooks not needed.

## Where it fails / limitations
- README's `useEffect` examples don't address React 18 **Strict Mode double-invocation** in dev; agents will be confused by "my mount logic runs twice".
- No mention of `useSyncExternalStore`, `useDeferredValue`, `useTransition`, `useId`, `useOptimistic` (React 18+/19) — agents reach for `useState` + `useEffect` instead.
- `useEffect` for data fetching is shown but anti-pattern in most modern apps — TanStack Query / SWR / Server Components are the right answer.
- Custom hook examples miss the **stale closure** trap when an effect captures props by reference — agents copy and ship subtle bugs.
- `useCallback`/`useMemo` shown without measuring; readers tend to memoize everything.
- No coverage of `useRef` for mutable values vs DOM nodes vs imperative handles (`useImperativeHandle`).
- Cleanup section doesn't cover async race conditions in effects — only the abort pattern.
- No guidance on `useReducer` vs many `useState` — README hints "consider useReducer" but doesn't show when.

## Agentic workflow
For each component task: (1) classify — server component (RSC) or client (`'use client'`)? (2) data flow — local state, derived, async, or external store? (3) prefer the simplest primitive (state → derived value → effect → custom hook → external store), (4) write component, (5) verify with React DevTools profiler if perf is in scope, (6) write tests using React Testing Library. Strict Mode ON in dev. Never silence ESLint `react-hooks/exhaustive-deps`; refactor instead.

### Recommended subagents
- `faion-code-agent` — Default for component + custom hook implementation.
- `faion-frontend-developer` (sibling skill) — Owns styling, accessibility, responsive layout.
- `faion-test-agent` — Writes RTL tests, asserts behavior not implementation.
- `faion-software-architect` — Decides global state library, server vs client split.
- `faion-sdd-execution` — Drives feature work where component is one task in a larger spec.

### Prompt pattern
New custom hook:

```
Create src/hooks/useDebounce.ts per
free/dev/software-developer/react-hooks/README.md.
Signature: function useDebounce<T>(value: T, delay: number): T.
Rules:
  - Cleanup with clearTimeout in effect return.
  - Exhaustive deps include `value` and `delay`.
  - Strict Mode safe (no side effect outside effect body).
Add tests/hooks/useDebounce.test.tsx using @testing-library/react renderHook
+ vi.useFakeTimers / jest.useFakeTimers.
Do not memoize the returned value beyond what useState provides.
```

Effect refactor:

```
Audit src/components/<Component>.tsx for:
  - useEffect with empty deps doing data fetch (replace with TanStack Query useQuery)
  - useState that can be derived from props/state (remove)
  - useCallback wrapping inline handlers passed to non-memoized children (remove)
  - missing cleanup in subscriptions/intervals
Apply minimal changes, no behavior change. Run vitest + tsc --noEmit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `react-devtools` | Inspect component tree, profiler | https://react.dev/learn/react-developer-tools |
| `eslint-plugin-react-hooks` | Enforce Rules of Hooks + exhaustive-deps | https://www.npmjs.com/package/eslint-plugin-react-hooks |
| `@testing-library/react` | RTL — test components | https://testing-library.com/docs/react-testing-library |
| `@testing-library/react-hooks` (deprecated, use RTL `renderHook`) | Test custom hooks in isolation | bundled in RTL 13+ |
| `vitest` | Fast test runner; first-class JSX/TSX | https://vitest.dev |
| `jest` + `ts-jest` / `babel-jest` | Alt test runner | https://jestjs.io |
| `tsc --noEmit` | TS check | bundled |
| `why-did-you-render` | Detect unnecessary re-renders in dev | https://github.com/welldone-software/why-did-you-render |
| `react-scan` | Visualize re-renders without instrumentation | https://react-scan.com |
| `eslint-plugin-react` (with `react/jsx-no-leaked-render`) | Catch JSX boolean-leak bug | https://www.npmjs.com/package/eslint-plugin-react |
| `npx storybook` | Component playground / visual testing | https://storybook.js.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| TanStack Query | OSS lib | Yes — replaces useEffect for fetching | Caches, retries, invalidations |
| SWR | OSS lib (Vercel) | Yes — simpler TanStack alt | Best for Next.js |
| Zustand | OSS lib | Yes — minimal store, no boilerplate | Compatible with `useSyncExternalStore` |
| Redux Toolkit | OSS lib | Yes — RTK Query for async | For complex state graphs |
| Jotai / Recoil | OSS lib | Yes — atom-based state | Fine-grained reactivity |
| React Hook Form | OSS lib | Yes — uncontrolled by default | Better perf than controlled state |
| Storybook Cloud | SaaS | Yes — visual regression | Pairs well with Chromatic |
| Chromatic | SaaS visual review | Yes — connects to Storybook | Component snapshot diffs |

## Templates & scripts
README has hook patterns. Add a Strict-Mode-safe `useFetch` example correcting README's data-fetching anti-pattern (≤45 lines):

```tsx
import { useEffect, useState } from "react";

type State<T> = { status: "idle" | "loading" | "success" | "error"; data?: T; error?: Error };

export function useFetch<T>(url: string): State<T> {
  const [state, setState] = useState<State<T>>({ status: "idle" });

  useEffect(() => {
    const ctrl = new AbortController();
    setState({ status: "loading" });
    fetch(url, { signal: ctrl.signal })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = (await r.json()) as T;
        setState({ status: "success", data });
      })
      .catch((err) => {
        if (err?.name === "AbortError") return; // ignore
        setState({ status: "error", error: err as Error });
      });
    return () => ctrl.abort();
  }, [url]);

  return state;
}
```

For real apps prefer TanStack Query — this is a teaching example showing correct cleanup and Strict-Mode-safe behavior.

## Best practices
- **Lift state up only when shared.** If two siblings need the same state, hoist; if not, keep local.
- **Derive instead of duplicate.** `const fullName = first + " " + last` beats a synced `useState(fullName)` + `useEffect`.
- **Custom hooks for shared *logic*, not shared *render*.** Render sharing → component composition.
- **Hooks rule the top.** Never inside `if`, loops, callbacks. ESLint plugin enforces.
- **`exhaustive-deps` ESLint rule is non-negotiable.** Missing deps = stale closures = hard bugs. If you genuinely don't want a dep, refactor to remove the need (extract function, use `useEvent` polyfill, or `useReducer`).
- **Cleanup every subscription, interval, observer.** Return cleanup from `useEffect`. React StrictMode mounts/unmounts/remounts in dev to catch missing cleanup — embrace it.
- **`useCallback` only when passing to a memoized child** (`React.memo`) or as a hook dep. Otherwise it's overhead with no benefit.
- **`useMemo` for expensive computations**, not for object identity stability of trivial values. React 19's compiler will obviate most of these.
- **`useRef` for mutable values that don't trigger render**, DOM refs, prior-value tracking. Don't read/write `.current` during render.
- **Server Components by default in Next.js App Router.** Add `'use client'` only at leaf interactive components.
- **Prefer libraries for: data fetching (TanStack Query), forms (RHF), animations (Framer Motion), routing (Next/TanStack Router).** Don't reinvent in `useEffect`.
- **Test behavior, not internals.** RTL's `getByRole` / `findByText`; never `wrapper.state()` (doesn't exist for hooks).
- **Use `React.startTransition` / `useTransition`** to deprioritize non-urgent updates (filter input → result list).

## AI-agent gotchas
- **Strict Mode dev double-invoke** — `useEffect`, refs initializer, state initializer all run twice in dev. Idempotent code works; "increment a counter on mount" doesn't.
- **Stale closure**: `useEffect(() => { setInterval(() => setCount(count + 1), 1000); }, [])` always sees `count = 0`. Use functional update `setCount(c => c + 1)` or include `count` in deps + cleanup.
- **`useEffect` racing async fetches**: response from previous URL arrives after URL change. Always abort or set a "current" flag in cleanup.
- **`exhaustive-deps` silenced** with `// eslint-disable-next-line` — the bug is now in the codebase forever. Fix the cause.
- **Non-primitive deps cause re-fires**: `useEffect(..., [{ a: 1 }])` re-runs every render. Memoize the object or destructure into primitives.
- **`useState(initialValue)` with expensive init** runs on every render. Use lazy form: `useState(() => compute())`.
- **`useMemo` returns stale value if deps don't change** — but if a dep is a `Date.now()` you reach for outside, it never updates. Move to a ref or recalc per render.
- **Conditional hooks** — even early `return null` before a hook call breaks the rule. ESLint catches; LLM agents sometimes do not.
- **Custom hook side-effects in body**: a hook that calls `fetch()` directly (not in `useEffect`) fires on every render. Wrap in effect.
- **`React.memo` + inline objects/functions as props** — memo is bypassed because reference changes each render. Pair with `useMemo`/`useCallback` or stable objects.
- **`useReducer` action types** lacking discriminated unions allow typo'd actions silently dispatching as no-op. Type as `Action = {type:"add"} | {type:"remove"; id: string}`.
- **`useImperativeHandle`** is a code smell unless wrapping a third-party imperative API. Most refs forwarding can be done via `forwardRef` alone.
- **Concurrent rendering tearing**: external mutable stores read directly during render produce inconsistencies. Always go through `useSyncExternalStore`.
- **`useEffect` for derived state** — re-render triggers effect, sets new state, re-renders again. Anti-pattern; compute during render.
- **Hydration mismatch**: SSR renders different output than client (e.g., `Date.now()` directly in JSX). Use `useEffect` to hydrate dynamic content.
- **Form state via `useState`**: many controlled inputs cause re-renders per keystroke. React Hook Form (uncontrolled) far faster.

## References
- README: `./README.md`
- React Docs (canonical): https://react.dev/reference/react
- Rules of Hooks: https://react.dev/warnings/invalid-hook-call-warning
- `useEffect` deep dive: https://react.dev/learn/synchronizing-with-effects
- "You Might Not Need an Effect": https://react.dev/learn/you-might-not-need-an-effect
- React 18 Strict Mode notes: https://react.dev/reference/react/StrictMode
- TanStack Query: https://tanstack.com/query
- React Hook Form: https://react-hook-form.com
- React Testing Library: https://testing-library.com/docs/react-testing-library
- Kent C. Dodds — React Hooks Pitfalls: https://kentcdodds.com/blog/react-hooks-pitfalls
- React Compiler (auto-memo): https://react.dev/learn/react-compiler
- eslint-plugin-react-hooks: https://www.npmjs.com/package/eslint-plugin-react-hooks
