# Tailwind Architecture

## Summary

**One-sentence:** Tailwind architecture spec: tokens in config (no arbitrary values), cn() everywhere via tailwind-merge, primitive extraction threshold (5 utils + 3 sites), @apply only in @layer components, prettier-plugin-tailwindcss for class order.

**One-paragraph:** Tailwind degenerates when arbitrary values bypass the token pipeline, when conditional class strings rely on raw clsx and conflicts silently win by source order, when chains are extracted too early (or never), when @apply leaks into component files defeating JIT, and when manual class reorder fights the formatter. This methodology produces an architecture spec: all design values in tailwind.config / @theme block; project cn() wrapping clsx + tailwind-merge with extendTailwindMerge; extraction threshold 5 utils + 3 call sites + named UI concept; @apply only in @layer components; prettier-plugin-tailwindcss for canonical class order.

**Ефективно для:**

- Перший Tailwind rollout - зафіксувати config, cn(), prettier-plugin-tailwindcss.
- Arbitrary values розповзаються (w-[347px]) - впровадити token policy.
- Conflict class issues (bg-red-500 vs bg-blue-500) - перейти на cn() через tailwind-merge.
- @apply використовується в component файлах - винести в @layer.
- Кожен PR переставляє класи - підключити prettier-plugin-tailwindcss.

## Applies If (ALL must hold)

- Codebase uses Tailwind CSS (v3 or v4).
- ESLint + Prettier are wired into the build pipeline.
- Team can refuse PRs that violate the token policy.
- Design system is in active growth (>20 components).

## Skip If (ANY kills it)

- Project uses CSS Modules or vanilla-extract instead of Tailwind.
- Tiny prototype with <5 components and no design tokens.
- Project is being migrated off Tailwind - lock the surface, do not invest.
- Team chose UnoCSS or similar - rule names differ.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design tokens | color / spacing / radius / shadow values | design |
| Tailwind version | v3 (config) or v4 (@theme) | engineering |
| ESLint config | .eslintrc with Tailwind plugin | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[shadcn-ui-architecture]] | primitive layer composed on top of Tailwind tokens. |
| [[react-component-architecture]] | feature-folder layout this spec presupposes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: tokens in config only, cn() wraps clsx+merge, extraction threshold, @apply only in @layer, prettier-plugin class order, extendTailwindMerge for custom, dark via semantic tokens | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: tokens, cn(), extraction threshold, @apply scope, formatter | ~900 |
| `content/05-examples.xml` | essential | Worked example for a Next.js + shadcn project | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `migrate-arbitrary-values` | sonnet | Per-occurrence judgement on which token replaces. |
| `wire-cn-util` | haiku | Boilerplate file. |
| `extract-primitive` | sonnet | Identify named UI concepts. |
| `audit-apply-usage` | sonnet | Component file scan + decision per occurrence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.ts` | Tailwind v3 config skeleton with design tokens + dark mode + safelist. |
| `templates/utils.ts` | Project cn() wrapping clsx + tailwind-merge with extendTailwindMerge. |
| `templates/cn.ts` | cn() helper: clsx + tailwind-merge composition for variants. |
| `templates/cva-variant-example.tsx` | cva variant authoring example: typed Variants + slot composition. |
| `templates/_smoke-test.json` | Minimum viable tailwind architecture artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind-architecture.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[shadcn-ui-architecture]]
- [[ui-component-library]]
- [[react-component-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - tokens source, cn() shape, extraction threshold, @apply scope - onto a rule from `content/01-core-rules.xml`. Use it before merging styling work: it catches arbitrary-values-creep and raw-clsx-conflicts upstream.
