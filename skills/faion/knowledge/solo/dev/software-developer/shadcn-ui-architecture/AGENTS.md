---
slug: shadcn-ui-architecture
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Architecture spec for shadcn/ui: components/ui/* as vendored primitives only, semantic CSS tokens, cva variants with compoundVariants, forwardRef + displayName, CODEOWNERS gate on primitive edits.
content_id: "dda34a472e5ef4b2"
complexity: medium
produces: spec
est_tokens: 4900
tags: [shadcn, react, ui, design-system, tailwind]
---
# shadcn/ui Architecture

## Summary

**One-sentence:** Architecture spec for shadcn/ui: components/ui/* as vendored primitives only, semantic CSS tokens, cva variants with compoundVariants, forwardRef + displayName, CODEOWNERS gate on primitive edits.

**One-paragraph:** shadcn/ui rots when business logic sneaks into `components/ui/*`, when concrete Tailwind shades replace semantic tokens in dark mode, when variant lists balloon to 12+ via flat cva, and when primitives are edited silently inside feature PRs. This methodology produces a spec: primitive vendoring rule, semantic-token vocabulary (`--background`, `--foreground`, etc.), cva + compoundVariants rules, mandatory forwardRef + displayName, and a CODEOWNERS gate on the primitive directory.

**Ефективно для:**

- Перший shadcn/ui rollout - зафіксувати primitive vs feature boundary.
- Variant explosion в Button (>6 variants) - перейти на compoundVariants.
- Dark mode виглядає неузгоджено - перейти на semantic tokens.
- Primitive edits всередині feature PR - впровадити CODEOWNERS.
- ref-passing не працює (Radix asChild) - винести forwardRef правило.

## Applies If (ALL must hold)

- Codebase uses React + Tailwind + shadcn/ui (vendored primitives).
- Design system is in active growth (new primitives + features regularly).
- Build pipeline supports CODEOWNERS + lint rules.
- Team can refuse PRs that violate primitive purity.

## Skip If (ANY kills it)

- Codebase uses a different design-system approach (MUI, Chakra, Mantine).
- Project is a tiny prototype with <10 components.
- Team chose Web Components or CSS-in-JS - shadcn vocabulary does not apply.
- Primitives are externally maintained (e.g. design-system as a separate package).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| shadcn primitive set | list of vendored primitives | design system |
| Token catalogue | CSS variable list under :root and .dark | design |
| Variant policy | max variants per prop (e.g. 6) | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind-architecture]] | shared token + cn() discipline. |
| [[react-component-architecture]] | primitive layer composed inside feature folder shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: primitives no business, CODEOWNERS gate, semantic tokens only, cva + compound, forwardRef+displayName, export variants fn, asChild slot | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: dir layout, tokens, variants, CODEOWNERS, lint | ~900 |
| `content/05-examples.xml` | essential | Worked example for a Next.js shadcn rollout | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-primitive-leakage` | sonnet | Per-import judgement. |
| `refactor-variants` | sonnet | Per-component cva re-design. |
| `wire-lint` | haiku | Boilerplate ESLint config. |
| `review-asChild-coverage` | opus | Stakes high; missing asChild breaks Radix slots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/button.tsx` | shadcn-style Button primitive with cva + compoundVariants + forwardRef + asChild. |
| `templates/globals.css` | Semantic token sheet for shadcn primitives. |
| `templates/_smoke-test.json` | Minimum viable shadcn architecture artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadcn-ui-architecture.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[tailwind-architecture]]
- [[react-component-architecture]]
- [[ui-component-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - primitive import shape, token kind, variant count, ownership gate - onto a rule from `content/01-core-rules.xml`. Use it before merging primitive edits: it catches business-in-primitive and variant-explosion upstream.
