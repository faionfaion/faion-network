# TypeScript Strict Mode

## Summary

**One-sentence:** tsconfig strict + 4 extras (noUncheckedIndexedAccess, exactOptionalPropertyTypes, noImplicitReturns, noFallthroughCasesInSwitch); Zod at IO; unknown over any.

**One-paragraph:** TypeScript strict mode is a compiler flag group (strict: true + four recommended extras) that eliminates implicit any, enforces null safety, catches unchecked index access, and requires explicit return types. The canonical 2026 baseline adds noUncheckedIndexedAccess, exactOptionalPropertyTypes, noImplicitReturns, noFallthroughCasesInSwitch on top of strict: true. IO boundaries are validated with Zod; unknown replaces any throughout.

**Ефективно для:** TS-інженера, який налаштовує tsconfig або робить strict-міграцію — закриває петлю між сирим any і Zod-валідованими границями.

## Applies If (ALL must hold)

- All new TypeScript projects.
- JS-to-TS migrations — adopt incrementally per directory.
- Strict-mode rollout in a partially typed codebase.
- Validating HTTP / queue / DB boundaries with Zod.

## Skip If (ANY kills it)

- Pure JS codebase with no TS plans.
- Tooling-only repo (Babel plugins, build configs) where TS overhead exceeds value.
- Generated code where types are upstream-owned.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| TypeScript 5.4+ installed | package | npm i -D typescript |
| tsconfig.json | JSON | repo root |
| Zod for IO validation | package | npm i zod |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | Foundational TS config methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: strict: true, the four extras, Zod at IO, unknown over any, no // @ts-ignore without code, explicit return types on exports. | ~1000 |
| `content/02-output-contract.xml` | essential | Shape: tsconfig.json with strict: true + four extras; Zod schemas at IO boundary; no any in src; no // @ts-ignore without reason. Forbidden: implicit any, // @ts-ignore bare. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: any everywhere, // @ts-ignore bare, narrowing without unknown, optional chaining over null check, Zod skipped at boundary. | ~800 |
| `content/04-procedure.xml` | medium | Steps: enable strict → enable four extras → eliminate any → add Zod at IO → enforce in CI. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: IO boundary? → Zod parse. Internal data? → discriminated union. Unknown shape? → unknown. Need any? → explain in comment. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-tsconfig` | haiku | Template fill. |
| `eliminate-any` | sonnet | Per-file judgement: unknown vs concrete type. |
| `design-zod-schemas` | sonnet | IO boundary modeling. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.json` | Canonical 2026 baseline with strict + four extras + module/moduleResolution. |
| `templates/zod-schema.ts` | Zod schema + parse function for an HTTP boundary. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-typescript-strict-mode.py` | Check tsconfig has strict + four extras; grep src for bare any and // @ts-ignore without code. | Pre-commit. |

## Related

- [[unit-testing]]
- [[storybook-setup]]
- [[tailwind]]

## Decision tree

The tree at content/06-decision-tree.xml routes between Zod parse, discriminated union, unknown, and (justified) any. Walk it whenever a new data shape crosses module or process boundaries.
