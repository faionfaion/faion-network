# React Decomposition

## Summary

**One-sentence:** Splits React components past 80 lines into custom hooks, feature folders, and service modules so each file fits an agent's working context.

**One-paragraph:** React components past ~80 lines collapse LLM editing accuracy. This methodology pulls non-render logic into custom hooks (`useX`), groups by feature (not by type), and pushes I/O into a thin services layer. Output is a per-component decomposition plan: identify render vs logic vs I/O, propose the new file tree, list the hooks to extract. The 80-line rule is a budget — past that, agents start guessing.

**Ефективно для:**

- React-репо з компонентами 300+ рядків: знизити cognitive load для людини + агента.
- Migration legacy class-based → functional + hooks.
- Storybook + test coverage: малі компоненти легше mock-ати.
- RSC (React Server Components): чітке розмежування server / client логіки.

## Applies If (ALL must hold)

- React project (functional components + hooks).
- At least one component &gt; 80 lines OR &gt; 200 LOC.
- Tests exist for current behaviour (so refactor stays safe).

## Skip If (ANY kills it)

- Class-based React legacy — different decomposition methodology (still useful but signature differs).
- Generated UI (auto-codegen from Figma) — splitting fights the generator.
- Tests broken — fix tests first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component file path | absolute | project tree |
| LOC + token count | integer | wc -l + tokenizer |
| Render vs logic vs I/O map | static analysis | manual or LSP |
| Test command | shell | package.json scripts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 80-line-budget, hooks-for-logic, feature-folders, services-for-io, test-between-moves | 1000 |
| `content/02-output-contract.xml` | essential | Schema for decomposition plan | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: prop-drilling-replaced-by-context, hooks-misused, by-type-folders | 700 |
| `content/04-procedure.xml` | essential | 5-step decomposition | 700 |
| `content/06-decision-tree.xml` | essential | Component shape tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_concerns` | sonnet | Per-component judgement. |
| `draft_plan` | sonnet | Maps concerns to hooks + services. |
| `execute` | haiku | Mechanical moves once plan is set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/useFeature.hook.ts` | Custom hook skeleton |
| `templates/feature-folder.tree.txt` | Feature-folder layout reference |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decomposition-react.py` | Validate decomposition plan + 80-line budget | Before applying moves |

## Related

- - [[code-decomposition-patterns]] — language-agnostic patterns this specialises.
- - [[javascript-modern]] — TS-strict + named-exports apply here too.

## Decision tree

See `content/06-decision-tree.xml`. Branches on what dominates the component: logic-heavy → extract hook. I/O-heavy → extract service. State-heavy → extract reducer + context. Multi-feature → split into feature folders.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/useFeature.hook.ts`

```typescript
import { useCallback, useEffect, useState } from 'react'

export interface UseFeatureOptions {
  initial?: unknown
  serviceFetch?: (id: string) => Promise<unknown>
}

export function useFeature(id: string, opts: UseFeatureOptions = {}) {
  const [data, setData] = useState(opts.initial ?? null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const reload = useCallback(async () => {
    if (!opts.serviceFetch) return
    setLoading(true); setError(null)
    try { setData(await opts.serviceFetch(id)) }
    catch (e) { setError(e as Error) }
    finally { setLoading(false) }
  }, [id, opts])

  useEffect(() => { reload() }, [reload])
  return { data, loading, error, reload }
}
```

### `templates/feature-folder.tree.txt`

```text
src/
├── features/
│   ├── billing/
│   │   ├── BillingPage.tsx         # ≤80 lines JSX
│   │   ├── useInvoiceFilter.ts     # hook
│   │   ├── useInvoiceList.ts       # hook
│   │   ├── invoiceApi.ts           # service (I/O)
│   │   ├── invoice.types.ts        # types
│   │   ├── __tests__/
│   │   │   └── BillingPage.test.tsx
│   │   └── index.ts                # public re-exports
│   └── auth/
│       └── ...
├── shared/                          # cross-feature reusables
│   ├── ui/
│   └── utils/
├── app/                             # router, providers, layout
└── main.tsx
```
