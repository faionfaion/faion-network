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

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-typescript-strict-mode.py` | Validate a migration spec against the contract. | After the spec is produced; before the first migration PR opens. |

## Related

- [[typescript-patterns]] — domain typing patterns the strict flags enforce.
- [[typescript-react-2026]] — App Router scaffold spec that assumes these flags are enabled.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree picks the per-error fix strategy: optional chain when the read is single-shot; destructure-with-default when iterating; assertion function when the call site guarantees presence; type predicate when narrowing unknown.
