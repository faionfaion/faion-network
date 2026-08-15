# React Hooks

## Summary

**One-sentence:** Produces a hooks-usage spec for a React 19 feature, mapping each piece of state to useState / useReducer / Context / external store with explicit cleanup and dependency-array rules.

**Ефективно для:** Designing a new React feature module where the agent must justify every hook choice (state shape, effect dependencies, memoization) instead of reflexively reaching for useState/useEffect everywhere.

**One-paragraph:** Turns the "which hook do I reach for here?" question into an auditable spec. The output names each piece of feature state, its hook (useState / useReducer / useContext / use() promise), the cleanup or AbortController owned by each effect, the dependency array for every effect, and the explicit decision either to memoize (with profiling rationale) or to skip memoization. Forbids conditional hook calls, raw async effect bodies, missing cleanup, and over-memoization of cheap computations. Output drives downstream codegen and PR review.

## Applies If (ALL must hold)

- Target is React 18.2 or 19+ with TypeScript strict mode.
- Component is functional (not a class component) and lives inside a feature module.
- State has clear ownership boundaries (local vs context vs external store) that need to be decided.
- The team agrees that hook choice is part of the design step, not "whatever the first dev typed".
- Output will be consumed by a codegen agent or a PR reviewer.

## Skip If (ANY kills it)

- Class components — use the React docs migration path instead.
- Server-state work where TanStack Query / SWR / RTK Query already owns caching.
- Global UI state already lives in Zustand / Jotai / Redux Toolkit — don't add a Context layer on top.
- Pure presentational component with zero state — just write JSX directly.
- React Native projects below RN 0.74 (hook compiler / Concurrent semantics differ).

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Feature brief | markdown | product / design doc |
| List of state slices (name, type, owner) | bullets | feature analysis pass |
| External-store inventory (Zustand/Jotai/Query) | YAML/JSON | repo config |
| React version | semver | `package.json` |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[react-patterns]]` | Component structure + Context provider pattern referenced by this spec. |
| `[[typescript-patterns]]` | Discriminated unions for reducer Action types. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 9 testable rules: hook call order, effect cleanup, no async effect body, functional updater, dep array primitives, memoize after profiling, derive-not-sync, ESLint gate at `error`, `use*` naming | ~1400 |
| `content/02-output-contract.xml` | essential | JSON schema for the hooks-usage spec + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: stale closure, conditional hook, object-literal deps, over-memoization, sync-via-effect, exhaustive-deps left at `warn` | ~950 |
| `content/04-procedure.xml` | medium | 6 steps: classify state → pick hook → declare deps + cleanup → memoize-or-not → emit spec → lock the lint gate | ~800 |
| `content/05-examples.xml` | medium | One worked example: SearchBox feature with useState + useDebounce + useEffect + AbortController | ~500 |
| `content/06-decision-tree.xml` | essential | Root: per state slice, which hook owns it? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `classify_state_slices` | haiku | Mechanical classification of slices into local/context/external. |
| `emit_hooks_spec` | sonnet | Bounded transformation: spec assembly from inputs. |
| `review_for_perf` | opus | Cross-checks memoization decisions against the profiling claim. |
| `lock_lint_gate` | sonnet | Install the flat-config block, classify the existing violation set, sequence the fixes. |

## Templates

| File | Purpose |
|---|---|
| `templates/hooks-spec.json` | Reference output document for one feature module. |
| `templates/useDebounce.ts` | Canonical custom hook with explicit return interface and cleanup. |
| `templates/useFetch.ts` | useEffect + AbortController + Result type example. |
| `templates/eslint-react-hooks.config.js` | Flat-config block setting `rules-of-hooks` and `exhaustive-deps` to `error` — the gate that keeps the codebase on the spec. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-react-hooks.py` | Validate a hooks-spec JSON against the output contract. | After the agent emits the spec, before codegen reads it. |

## Related

- [[react-patterns]] — broader React feature-structure decisions consumed here.
- [[typescript-react-2026]] — Server Component boundaries that gate where hooks may live.
- [[typescript-patterns]] — Result + discriminated unions used by useReducer Actions.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree walks every state slice through ownership (server / form / global UI / local) and, when local, through shape (single value / multi-field interrelated / boolean flag) — each leaf binds the slice to a concrete hook plus the rule id explaining the choice. Run it once per slice before emitting the spec.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/hooks-spec.json`

```json
{
  "_purpose": "Reference hooks-usage spec output for one React feature module.",
  "_consumes": "Feature brief + state slices + external store inventory.",
  "_produces": "JSON consumed by a codegen agent or a PR reviewer.",
  "_depends-on": "content/02-output-contract.xml schema.",
  "_token-budget-impact": "~150 tokens.",
  "artefact_id": "search-box-hooks",
  "owner": "ruslan@faion.net",
  "feature_name": "search-box",
  "react_version": "^19.0.0",
  "state_slices": [
    {
      "name": "query",
      "owner_hook": "useState",
      "type": "string",
      "rule_ref": "r4-functional-updater"
    },
    {
      "name": "debouncedQuery",
      "owner_hook": "useState",
      "type": "string",
      "rule_ref": "r2-effect-cleanup"
    },
    {
      "name": "results",
      "owner_hook": "tanstack-query",
      "type": "SearchResult[]"
    }
  ],
  "effects": [
    {
      "name": "debounce-query",
      "deps": [
        "query"
      ],
      "cleanup_present": true,
      "uses_abort_controller": false
    },
    {
      "name": "fetch-search-results",
      "deps": [
        "debouncedQuery"
      ],
      "cleanup_present": true,
      "uses_abort_controller": true
    }
  ],
  "memoization": [],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/useDebounce.ts`

```typescript
import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    // Mandatory cleanup: cancels the previous timer when value or delayMs changes,
    // or when the component unmounts. Required by rule r2-effect-cleanup.
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}
```

### `templates/useFetch.ts`

```typescript
import { useEffect, useState } from 'react';

type FetchState<T> =
  | { state: 'idle' }
  | { state: 'loading' }
  | { state: 'ok'; data: T }
  | { state: 'error'; error: Error };

export function useFetch<T>(url: string): FetchState<T> {
  const [result, setResult] = useState<FetchState<T>>({ state: 'idle' });

  useEffect(() => {
    const controller = new AbortController();
    setResult({ state: 'loading' });

    async function run(): Promise<void> {
      try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as T;
        setResult({ state: 'ok', data });
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setResult({ state: 'error', error: err });
        }
      }
    }

    void run();
    // Cancels the in-flight fetch on unmount or url change. Required by r2 + r3.
    return () => controller.abort();
  }, [url]);

  return result;
}
```
