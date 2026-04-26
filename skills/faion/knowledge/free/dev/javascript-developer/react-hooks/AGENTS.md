# React Hooks

Functional component patterns using React's built-in hooks — state, effects, memoization, refs, reducers, context, and reusable custom hook extraction.

## Why

Hooks are the only state/lifecycle mechanism in modern React. Misusing them (stale closures, missing cleanup, over-memoization, conditional calls) causes subtle bugs that are hard to diagnose.

## When To Use

- All functional components needing local state or side effects
- Extracting reusable stateful logic into custom hooks
- Performance optimization via memoization (with profiling first)
- Sharing state across a component tree via Context

## When NOT To Use

- Class components (use the React docs migration path)
- Logic that belongs in a state manager (Zustand, TanStack Query) — don't replicate server cache or global UI state with local hooks

## Content

| File | What's inside |
|------|---------------|
| `content/01-state-ref.xml` | useState patterns (object/lazy init), useRef (DOM, mutable value, stable callback) |
| `content/02-effects.xml` | useEffect with cleanup, AbortController data fetching, callbackRef pattern |
| `content/03-memoize.xml` | useCallback and useMemo rules, useReducer for complex state |
| `content/04-custom-context.xml` | Custom hook shape (useFetch, useDebounce), Context+hook provider pattern |

## Templates

none
