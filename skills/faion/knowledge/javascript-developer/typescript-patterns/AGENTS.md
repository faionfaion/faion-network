# TypeScript Patterns

## Summary

**One-sentence:** Produces a typed-shapes spec — generic interfaces, discriminated-union Result types, Zod schemas + inferred types, type guards / asserts — that an agent uses as the type contract for a TS strict codebase.

**Ефективно для:** Greenfield service or library design where the team wants to encode domain invariants in the type system instead of asserting them at runtime, and where unknown external input (API bodies, env, form data) must be validated before crossing trust boundaries.

**One-paragraph:** Replaces ad-hoc `as` casts and `any` with a documented contract. The output lists each domain type with its shape (interface or schema), its parse strategy (Zod parse vs safeParse vs assertion function), its discriminated-union variants where applicable, and its branding decision (for IDs that share string as the underlying type). Forbids `Meta.fields = '__all__'`-style implicit exposure, unchecked indexed access, non-null assertions on legitimately nullable values, and untyped `any` boundaries.

## Applies If (ALL must hold)

- TypeScript ≥ 5.0 with strict mode + noUncheckedIndexedAccess + exactOptionalPropertyTypes enabled.
- Codebase processes external input (HTTP bodies, env, queue messages, form data) at trust boundaries.
- The team agrees that domain invariants belong in types, not in scattered runtime checks.
- A validation library is available (Zod / Valibot / ArkType) or can be added.
- Output drives codegen and PR review.

## Skip If (ANY kills it)

- Prototype / spike code being thrown away within the week.
- Pure plumbing code with no domain concepts (build tools, simple CLI wrappers).
- The codebase already uses runtime-validated types (e.g., Effect Schema) consistently — don't add a parallel system.
- Team explicitly chose duck typing for speed; the spec adds friction without value.
- One-off scripts where type generics noise outweighs benefit.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Domain glossary | markdown | product doc |
| External-input inventory (endpoints, env vars, queues) | YAML | architecture doc |
| TS version + strict flags | tsconfig.json | repo root |
| Chosen validation library | string | repo decision record |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[typescript-strict-mode]]` | Strict flags this spec assumes are enabled. |
| `[[typescript-react-2026]]` | Server / client boundary that drives where Zod schemas live. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: utility types over hand-rolled, discriminated unions over nullable returns, Zod-inferred types, branded IDs, type guards over casts, asserts narrowers, no-`any` boundaries | ~1100 |
| `content/02-output-contract.xml` | essential | JSON schema for the typed-shapes spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: `any` at boundaries, `as` casts on unknown, `!` chains, schema drift | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: enumerate domain types → pick representation → declare validators → brand IDs → emit spec | ~600 |
| `content/05-examples.xml` | medium | One worked example: Order domain with Result + Zod + UserId/OrderId brands | ~500 |
| `content/06-decision-tree.xml` | essential | Per-type tree: external input? → Zod. internal? → interface. nullable return? → Result. ID-of-string? → brand | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_domain_types` | haiku | Mechanical extraction from the glossary. |
| `emit_typed_spec` | sonnet | Bounded transformation of types to spec entries. |
| `review_for_security` | opus | Cross-checks: which types cross trust boundaries vs internal? |

## Templates

| File | Purpose |
|---|---|
| `templates/repository.ts` | Generic Repository&lt;T, ID&gt; interface; baseline for CRUD shapes. |
| `templates/result.ts` | Discriminated-union Result + assertDefined helper. |
| `templates/zod-user.ts` | UserSchema + z.infer + validators reference. |
| `templates/typed-shapes-spec.json` | Reference output document. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-typescript-patterns.py` | Validate a typed-shapes spec JSON against the contract. | After the agent emits the spec. |

## Related

- [[typescript-strict-mode]] — sets the compiler flags this methodology assumes.
- [[typescript-react-2026]] — drives where schemas live across server/client boundary.
- [[react-hooks]] — Result types consumed by useReducer Action unions.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree routes each domain type by trust boundary (external input → Zod-validated schema; internal-only → plain interface), by failure modality (nullable result → Result discriminated union; throwing failure → assertion function), and by identity uniqueness (ID-of-string → branded type).
