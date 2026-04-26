# React Patterns

## Summary

Modern React patterns for production apps: feature-based folder structure, typed functional components, custom hooks, Context provider pattern, state management decision tree, and performance memoization rules. All patterns assume React 18+ with TypeScript strict mode.

## Why

React's flexibility makes it easy to write hard-to-maintain code. These patterns enforce consistent colocated state, prevent prop-drilling via Context, and ensure memoization is applied only where measured — avoiding the common trap of over-optimizing.

## When To Use

- Building a new React feature module (auth, dashboard, checkout)
- Deciding where to put state (server vs. local vs. global)
- Extracting reusable async data-fetching logic into a custom hook
- Wrapping third-party state in a typed Context provider
- Optimizing a component that profiling shows as a bottleneck

## When NOT To Use

- Simple presentational components with no state — just write JSX
- When TanStack Query is already in use for server state — don't duplicate with useEffect fetching
- When Zustand already handles global UI state — don't add a Context layer on top

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Feature-based folder layout, component anatomy rules |
| `content/02-hooks-context.xml` | Custom hook with typed return, Context provider pattern with runtime check |
| `content/03-state-perf.xml` | State management decision tree, memoization rules, anti-patterns |

## Templates

none
