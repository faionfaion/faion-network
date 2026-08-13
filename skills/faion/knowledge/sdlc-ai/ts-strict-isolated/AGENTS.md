# TypeScript Strict + isolatedDeclarations + Project References

## Summary

**One-sentence:** Every tsconfig.json must enable strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes; libraries add isolatedDeclarations + composite + references so fast emitters (Biome/oxc/swc) produce .d.ts without invoking tsc.

**One-paragraph:** Every tsconfig.json in a TypeScript workspace must enable `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`, and (for libraries / shared packages) `isolatedDeclarations: true` plus `composite: true` with references to its dependency packages. This raises compile-time precision so that AI-generated code surfaces type errors instead of runtime bugs, and lets fast emitters (Biome, oxc, swc) produce `.d.ts` without invoking tsc for inference.

**Ефективно для:**

- AI-генерований TS, де inferred types ховають bugs.
- Monorepo з декількома packages — composite/refs prevent cycles.
- Biome/oxc/swc emitters: isolated declarations потрібні для emit.
- Onboarding strict mode: tsconfig.base.json як floor.

## Applies If (ALL must hold)

- TypeScript project where AI-generated code is committed.
- Monorepo with multiple packages that share types.
- Build performance matters (large monorepo using a fast emitter).

## Skip If (ANY kills it)

- Project is plain JS with no TS plans.
- Single-file `.ts` script with no shared types.
- Codebase actively uses `any` as a design choice (deferred typing).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| tsconfig.json baseline | config | repo |
| Package layout (monorepo or single) | filesystem | repo |
| Fast emitter choice (Biome / oxc / swc / tsc) | decision | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.base.json` | Root tsconfig with strict + noUnchecked + exactOptional flags. |
| `templates/tsconfig.lib.json` | Library tsconfig extending base, with isolatedDeclarations + composite + references. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ts-strict-isolated.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[uv-lockfile-floor]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tsconfig.base.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "target": "ES2023",
    "lib": [
      "ES2023"
    ],
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": false,
    "verbatimModuleSyntax": true,
    "resolveJsonModule": true,
    "useDefineForClassFields": true
  }
}
```

### `templates/tsconfig.lib.json`

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "isolatedDeclarations": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src",
    "tsBuildInfoFile": "dist/.tsbuildinfo"
  },
  "include": [
    "src"
  ],
  "exclude": [
    "dist",
    "node_modules",
    "**/*.test.ts"
  ],
  "references": [
    {
      "path": "../shared"
    }
  ]
}
```
