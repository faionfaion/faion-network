# Agent Integration — TypeScript Patterns

## When to use
- Tightening type safety across an existing TS codebase: `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`.
- Designing a new public API (library, SDK, internal package) where consumers depend on exact types.
- Refactoring a module to leverage discriminated unions, branded types, or template literal types.
- Replacing runtime-throwing code with type-narrowing (type guards, assertion functions).
- Eliminating `any` and `as` casts during a code-quality push.
- Generic-heavy abstractions (Repository, Result, Either, Reader) where bounds and inference matter.
- Schema-first API codegen: aligning Zod / Valibot / Effect-Schema with TS types via `z.infer`.

## When NOT to use
- Quick scripts and one-off automations (`tsx` + minimal types is fine).
- Code that crosses the FFI boundary (WASM, native modules) — type the wrapper, not internals.
- Framework boilerplate where the framework already supplies precise types (Next.js route handlers, tRPC procedures).
- Migration phase where strictness causes a flood of errors — fix the high-leverage rules first, defer the rest.
- Performance-critical hot paths where complex generics slow `tsc --noEmit` to a crawl.

## Where it fails / limitations
- README presents strict-mode flags as on/off but doesn't address which to enable first; agents flip everything and produce thousands of errors.
- Generic-heavy patterns can blow `tsc` perf — README has no compile-time-cost guidance.
- Type guards and assertion functions look interchangeable but only assertion functions narrow control flow without `if`; agents pick the wrong one.
- `Awaited<T>` and conditional types are shown but inference traps (distributive vs non-distributive) aren't.
- Branded types (`type UserId = string & { __brand: 'UserId' }`) are mentioned but no constructor pattern (`asUserId(s: string): UserId`) or runtime-validation pairing.
- Discriminated unions need `never` exhaustiveness checks; README likely shows the union but not the `assertNever` helper.
- `as const` and `satisfies` are easily confused; agents mix them and lose narrowing.
- Module augmentation and declaration merging skipped — common need for typing third-party packages.

## Agentic workflow
For new code: prompt agent to declare types **before** function bodies, use `satisfies` for inferred-but-checked literals, and reach for `unknown` instead of `any` when uncertain. For refactor: enable one strict flag per PR, fix all errors, then enable the next. Use a reviewer subagent that bans `as`, `any`, and non-null assertions (`!`) outside explicitly-allowed paths (test fixtures, migrations). Pair generation with `tsc --noEmit` between steps; refuse a diff if `tsc` errors increase.

### Recommended subagents
- `faion-frontend-developer` / `faion-javascript-developer` — primary writers; pair with a TS-strict reviewer.
- Reviewer subagent — scans diffs for `any`, `as`, `!`, `// @ts-ignore`, `// @ts-expect-error` without justification.
- `faion-software-architect` — chooses generic abstractions and module boundaries (Result, Repository, Brand).
- `faion-sdd-execution` — tracks strict-flag enablement as separate quality gates per release.

### Prompt pattern
```
TS conventions in this repo:
- strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes ON.
- No `any`, no `as` outside parsing layer.
- Use `unknown` + type guard for external input.
- Discriminated unions for state machines; assertNever in default case.
- Branded types for IDs (UserId, OrderId), constructed via parse functions.
- `satisfies T` for inferred-but-checked config literals.

Implement <module> following the conventions. Run `tsc --noEmit`, expected: 0 errors.
```

```
Audit-only: scan src/ for:
- `: any`, `as unknown as`, `!.`, `// @ts-ignore`.
- Functions returning `boolean` that should be type predicates.
- Switch statements over discriminated unions missing `assertNever`.
Output JSON list with file:line, kind, suggested fix. Do not edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsc --noEmit` | Type-check without compile output | https://www.typescriptlang.org |
| `tsc --watch` | Continuous type-check during dev | bundled |
| `eslint` + `@typescript-eslint` | Lint TS-specific anti-patterns | https://typescript-eslint.io |
| `tsd` / `expect-type` | Type-level unit tests | https://github.com/SamVerschueren/tsd |
| `zod` / `valibot` / `effect-schema` | Runtime parsing aligned with TS types | https://zod.dev / https://valibot.dev |
| `ts-prune` / `knip` | Find unused exports / dead types | https://github.com/webpro/knip |
| `type-coverage` | Track % of typed expressions | https://github.com/plantain-00/type-coverage |
| `arethetypeswrong` | Validate published package types | https://arethetypeswrong.github.io |
| `tsx` | Run TS files directly without build | https://github.com/privatenumber/tsx |
| `pkg-types` | Inspect published types from registries | https://github.com/unjs/pkg-types |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes | `tsc --noEmit` per PR; cache `~/.npm` and `node_modules` |
| GitLab CI | CI | Yes | Same, with `node:` image |
| Codecov | SaaS | Yes | Coverage works at runtime; for types use `type-coverage` separately |
| `@changesets/cli` | OSS | Yes — CLI driveable | Versioning that respects type-only breaking changes |
| Are The Types Wrong | SaaS + CLI | Yes | Validate dual ESM/CJS type exports for libraries |
| Renovate / Dependabot | SaaS | Yes | Track `@types/*` and `typescript` upgrades; type errors surface in PR |

## Templates & scripts
See `templates.md` for `tsconfig.json`, branded type helpers, and Result/Either utilities. Inline branded ID with safe constructor:

```ts
// src/types/branded.ts
declare const __brand: unique symbol;
export type Brand<T, B> = T & { readonly [__brand]: B };

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function asUserId(s: string): UserId {
  if (!UUID_RE.test(s)) throw new TypeError(`Invalid UserId: ${s}`);
  return s as UserId;
}

export function isUserId(s: string): s is UserId {
  return UUID_RE.test(s);
}

// Exhaustiveness helper
export function assertNever(x: never, ctx = 'unreachable'): never {
  throw new Error(`${ctx}: ${JSON.stringify(x)}`);
}
```

## Best practices
- **`unknown` over `any`** for external input; narrow with type guards or schema parse.
- **`satisfies T` over `: T`** for config literals — keeps narrowing while validating shape.
- **Discriminated unions for state.** `type State = { kind: 'idle' } | { kind: 'loading' } | { kind: 'error', err: Error } | { kind: 'ok', data: T }` then exhaustive `switch` + `assertNever`.
- **Branded types for entity IDs.** Prevents passing `UserId` where `OrderId` is expected, even though both are strings.
- **Schema at the edge.** Parse external input (HTTP body, env vars, config files) with Zod/Valibot, infer types from schemas, internal code uses inferred types.
- **No `as` casts inside business logic.** Allowed only at the parsing seam (API boundary, env config).
- **Generics with constraints**: `<T extends { id: string }>` beats unconstrained `<T>` — enables property access and inference.
- **`Readonly<T>` and `ReadonlyArray<T>`** for parameters that shouldn't be mutated; surfaces mistakes at compile time.
- **`Pick`, `Omit`, `Partial`, `Required`** — compose; don't redefine.
- **Path aliases (`@/`)** with project references for monorepos; speeds incremental builds.
- **Type coverage > 95%** — use `type-coverage --strict` in CI to block regressions.

## AI-agent gotchas
- **`any` slips in** as a fix for "type error" — agents prefer expediency. Lint-rule `@typescript-eslint/no-explicit-any: error`.
- **`as unknown as T` double cast** to silence errors — same as `any`. Ban via lint or PR review.
- **Non-null assertion (`!`)** appearing in business logic — usually means narrowing is missing. Allowed only in tests with explicit comment.
- **`Object.keys(obj)` returns `string[]`**, not `(keyof T)[]`. Agents iterate and access typed properties via the loop var; need `(Object.keys(obj) as (keyof T)[])` cast deliberately or `Object.entries`.
- **Distributive conditional types**: `type IsString<T> = T extends string ? true : false` distributes over unions. Wrap `[T]` to prevent: `type IsString<T> = [T] extends [string] ? true : false`.
- **`Awaited<T>` over `T`**: agents sometimes await non-Promise values then complain types are wrong; use `Awaited<ReturnType<typeof fn>>` for async return.
- **Type guards that compare to `null`**: `function isUser(x: unknown): x is User { return x !== null }` — narrows to `{}`, not `User`. Need structural check.
- **Mutating frozen / readonly types** — TS won't error on runtime mutation if cast escapes; tests catch this, types alone don't.
- **`enum` vs union of literals**: agents reach for `enum` (TS-specific, runtime cost). Prefer `as const` arrays or string-literal unions; only use `enum` for legacy interop.
- **Module augmentation paths**: `declare module 'foo'` requires the file to be a module (has `import`/`export`); agents put augmentation in `.d.ts` without ensuring it's loaded by `tsconfig`.
- **`import type` vs `import`**: agents mix; type-only imports don't bundle but are stripped — using a type-only import as a runtime value gives "is not defined".
- **Excess property checks** only fire on object literals; agents pass a variable and lose the check.
- **`tsc --noEmit` perf cliff**: a few `infer` chains + recursive types can spike compile to 60s. Use `tsc --extendedDiagnostics` to find offenders.
- **Human-in-loop checkpoint**: any new generic with > 3 type parameters; usually a sign of insufficient design.

## References
- README: `./README.md`
- Sibling: `../typescript-strict-mode/`, `../react-hooks/`, `../typescript-react-2026/`, `../nodejs-express/`
- TS Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- TS-ESLint rules: https://typescript-eslint.io/rules/
- Zod: https://zod.dev
- Effect: https://effect.website
- Matt Pocock — Total TypeScript: https://www.totaltypescript.com
- Anders Hejlsberg — Discriminated Unions talk: https://www.youtube.com/watch?v=ifLL0L_HreQ
- Are The Types Wrong: https://arethetypeswrong.github.io
- Type-Coverage: https://github.com/plantain-00/type-coverage
