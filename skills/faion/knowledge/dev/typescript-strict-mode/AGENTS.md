# TypeScript Strict Mode

## Summary

**One-sentence:** Produces a strict-mode adoption spec listing the compiler flags to enable (strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes + …), the migration order (one flag per PR), and the lint rules that backstop common workarounds.

**Ефективно для:** Greenfield project that wants strict from day one, OR a brownfield codebase planning an incremental migration where each strict flag is its own PR with a fix budget.

**One-paragraph:** Turns the question "which strict flags do we enable and in what order?" into an auditable spec. The output lists every flag to enable, the per-flag fix strategy (e.g., for noUncheckedIndexedAccess: destructure with default, optional chain, length check), and the backstop ESLint rules (no-non-null-assertion on indexed access, no-explicit-any on exports). Forbids `!` chains on nullable values, `as T` on unknown input, missing `unknown` at trust boundaries, and `@ts-expect-error` to suppress strict-flag errors.

## Applies If (ALL must hold)

- TypeScript ≥ 5.0.
- Codebase has either (a) zero strict flags set, or (b) a partial set the team wants to complete.
- The team has buy-in to merge "one flag = one PR" rather than flip everything at once.
- A clear owner exists for the migration plan.
- Output drives a tracked migration backlog.

## Skip If (ANY kills it)

- Auto-generated code (protobuf, OpenAPI client stubs) — `@ts-nocheck` per file is the right tool.
- Throwaway script or one-off automation where strict noise outweighs benefit.
- Codebase already at the 2026 baseline (strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes) — nothing to do.
- Team explicitly chose loose typing for velocity — methodology adds friction.
- Library where strictness conflicts with required d.ts emit shape (rare; document the exception).

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Current tsconfig.json | JSON | repo root |
| `tsc --noEmit` error count baseline | text | CI log |
| Migration owner | handle/email | decision record |
| Acceptable error budget per PR | int | team agreement |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[typescript-patterns]]` | Result + assertion functions consumed in the per-flag fix strategies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: strict on, noUncheckedIndexedAccess on, exactOptionalPropertyTypes on, no-bang-chain, no-as-cast, unknown at boundary | ~1000 |
| `content/02-output-contract.xml` | essential | JSON schema for the migration spec | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: bang chain, as-on-unknown, ts-expect-error suppress, big-bang migration | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: baseline → enable strict → enable noUnchecked → enable exact-optional → backstop lint | ~600 |
| `content/05-examples.xml` | medium | One worked example: migrating a service file through each flag | ~500 |
| `content/06-decision-tree.xml` | essential | Per error: optional chain vs assertion fn vs destructure default | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `baseline_errors` | haiku | Mechanical: run tsc, count errors, classify. |
| `emit_migration_plan` | sonnet | Per-flag PR plan with fix strategies. |
| `review_for_lint_backstops` | opus | Cross-checks ESLint config against the fix strategies. |

## Templates

| File | Purpose |
|---|---|
| `templates/tsconfig.strict.json` | TS 5.x strict baseline tsconfig. |
| `templates/migration-spec.json` | Reference migration spec output. |
| `templates/.eslintrc.strict-backstop.json` | ESLint rules that backstop common workarounds. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-typescript-strict-mode.py` | Validate a migration spec against the contract. | After the spec is produced; before the first migration PR opens. |

## Related

- [[typescript-patterns]] — domain typing patterns the strict flags enforce.
- [[typescript-react-2026]] — App Router scaffold spec that assumes these flags are enabled.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree picks the per-error fix strategy: optional chain when the read is single-shot; destructure-with-default when iterating; assertion function when the call site guarantees presence; type predicate when narrowing unknown.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tsconfig.strict.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "target": "ES2022",
    "lib": [
      "ES2022",
      "DOM",
      "DOM.Iterable"
    ],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

### `templates/migration-spec.json`

```json
{
  "_purpose": "Reference strict-mode migration spec output.",
  "_consumes": "tsconfig.json + tsc baseline + owner.",
  "_produces": "JSON for migration backlog.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~150 tokens.",
  "artefact_id": "billing-strict-migration",
  "owner": "ruslan@faion.net",
  "repo": "faion-net-be",
  "ts_version": "^5.4.0",
  "current_flags": {
    "strict": false
  },
  "target_flags": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  },
  "migration_steps": [
    {
      "order": 1,
      "flag": "strict",
      "fix_strategy": "Enable bundle; address strictNullChecks errors by adding | undefined to optional returns and explicit return types.",
      "error_budget": 80
    },
    {
      "order": 2,
      "flag": "noUncheckedIndexedAccess",
      "fix_strategy": "Destructure with default OR optional chain at every array[i] / record[key] read site.",
      "error_budget": 80
    },
    {
      "order": 3,
      "flag": "exactOptionalPropertyTypes",
      "fix_strategy": "Audit optional fields; add | undefined where explicit undefined assignment is part of the contract.",
      "error_budget": 30
    }
  ],
  "lint_backstops": [
    "@typescript-eslint/no-non-null-assertion",
    "@typescript-eslint/no-explicit-any",
    "@typescript-eslint/no-unsafe-assignment",
    "@typescript-eslint/ban-ts-comment"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/.eslintrc.strict-backstop.json`

```json
{
  "_purpose": "ESLint backstop rules that prevent regressions of TS strict mode wins.",
  "_consumes": "nothing \u2014 extend in repo .eslintrc.",
  "_produces": "rule set.",
  "_depends-on": "@typescript-eslint/eslint-plugin >= 7.",
  "_token-budget-impact": "~80 tokens.",
  "extends": [
    "plugin:@typescript-eslint/recommended-type-checked"
  ],
  "rules": {
    "@typescript-eslint/no-non-null-assertion": "error",
    "@typescript-eslint/no-explicit-any": [
      "error",
      {
        "ignoreRestArgs": false
      }
    ],
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-return": "error",
    "@typescript-eslint/ban-ts-comment": [
      "error",
      {
        "ts-expect-error": true,
        "ts-ignore": true,
        "ts-nocheck": "allow-with-description"
      }
    ]
  }
}
```
