# Agent Integration — TypeScript Strict Mode

## When to use
- All new TypeScript codebases — strict mode is the only sane default for production code.
- Migrating a JS codebase — adopt strict in stages (`strict: true` → `noImplicitAny` → `strictNullChecks` per directory).
- Library / SDK development — published `.d.ts` strictness is part of API quality.
- LLM-authored code — strict mode is the cheapest static gate against hallucinated APIs and `any` leaks.
- Multi-team monorepos where shared types are the integration contract.
- Critical paths (auth, billing, IAM, parsing) where null/undefined bugs are unacceptable.

## When NOT to use
- Throwaway prototypes / spike branches — strict mode doubles iteration cost when you'll discard the code.
- Bridging legacy JS where every file fights `noImplicitAny` — adopt incrementally via `// @ts-check` on JS files first.
- Codebases that depend on poorly typed third-party libs without `@types/*` — `skipLibCheck: true` + targeted `unknown` adapters first.
- Highly dynamic plugin systems where types fight extension hooks; structural alternatives (Zod schemas + parse boundaries) cleaner.

## Where it fails / limitations
- **Migration debt.** Toggling `strict: true` on a 50K-line codebase yields thousands of errors; agents can't fix in one PR. Use `--noEmitOnError false` + per-file `// @ts-strict-ignore` (with a sunset deadline) and migrate incrementally.
- **`any` leaks via untyped libs.** A single `import { foo } from 'untyped-pkg'` poisons downstream types. Always wrap with a typed adapter and `@types/*` declaration.
- **`noUncheckedIndexedAccess`** trips agents who don't handle `T | undefined` after array indexing. Real bug catches; ergonomics suffer until adopted.
- **`exactOptionalPropertyTypes`** breaks libraries that pass `undefined` for optional props (React especially). Audit lib compatibility before flipping.
- **`strictPropertyInitialization`** fights DI frameworks (Nest.js, TypeORM); use `!` definite-assignment or `init` patterns.
- **Type assertions (`as`)** silently bypass strictness; LLMs reach for `as` to "fix" type errors. Lint rule `@typescript-eslint/no-unsafe-*` catches; but enforcement needed.
- **`@ts-ignore` rot.** Ignored errors accumulate with no expiry. Use `@ts-expect-error` (errors out when no longer needed) and require a comment.
- **Module resolution drift.** `verbatimModuleSyntax`, `isolatedModules`, `moduleResolution: "bundler"` are version-sensitive; mismatched bundler/TS combos produce confusing errors.
- **Decorator types.** Strict mode + experimental decorators (Nest, TypeORM) needs `experimentalDecorators` + `emitDecoratorMetadata`; agents don't always wire correctly.
- **Performance.** Large strict projects with project references compile slower than non-strict. Use `tsc --build` + incremental + `--pretty false` in CI.

## Agentic workflow
Drive strict-mode work in 4 stages: (1) a **migration-planner** subagent runs `tsc --strict --noEmit` on the codebase, buckets errors by file/rule, and emits a phased plan (per-rule or per-directory); (2) a **per-file-fixer** subagent works one file at a time, eliminating `any` / `!` / `as` non-trivially (refactoring, not silencing); (3) a **type-guard-author** subagent creates `is*` guards and Zod / valibot parsers at IO boundaries (req/res, JSON, env); (4) a **lint-rule-tightener** subagent ratchets ESLint rules (`no-explicit-any: error`, `no-non-null-assertion: error`) once green. Always run `tsc --noEmit && eslint . --max-warnings 0` in CI; LLMs commonly add code that compiles but lints dirty.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `pnpm typecheck && pnpm lint && pnpm test`.
- A purpose-built **strict-migration-agent** (worth creating): given a `tsc` error list, groups by rule and proposes file-level fixes (with diff suggestions).
- A **any-hunter-agent** (worth creating): grep-driven; finds `any`, `as any`, `@ts-ignore`, `@ts-expect-error` and ranks by blast radius.
- A **zod-boundary-agent** (worth creating): for any function consuming external data (HTTP, fs, env), proposes a Zod schema + `parse()` so downstream code can be strictly typed.
- A **type-test-agent** that runs `tsd` / `expect-type` to assert public API types stay stable across releases.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub secrets from `.env`, fixture types before commit.

### Prompt pattern
Per-file fix:
```
File: src/users/service.ts. tsc --strict reports 12 errors.
For each error:
1. Identify root cause (real bug vs missing annotation)
2. Refactor — do NOT add `as`, `!`, or `any`
3. Prefer `unknown` + type guard over `any`
4. Use Zod for runtime IO validation
Output the full updated file.
Constraints: no @ts-ignore, no @ts-expect-error.
Verify: pnpm tsc --noEmit src/users/service.ts.
```

Boundary parsing:
```
For function loadConfig() that reads process.env, define a
ConfigSchema with zod:
- DATABASE_URL: z.string().url()
- PORT: z.coerce.number().int().positive().default(3000)
- LOG_LEVEL: z.enum(['debug','info','warn','error']).default('info')
loadConfig() returns z.infer<typeof ConfigSchema>; throws on
parse error with helpful message. Add tests for missing/invalid.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsc` | TypeScript compiler / typechecker | https://www.typescriptlang.org |
| `tsx` / `ts-node` | Run TS directly | https://github.com/privatenumber/tsx |
| `@typescript-eslint/parser` + `eslint-plugin` | Lint TS rules | https://typescript-eslint.io |
| `tsd` | Test types | https://github.com/SamVerschueren/tsd |
| `expect-type` | Type-level assertions | https://github.com/mmkal/expect-type |
| `type-coverage` | Measure % of fully typed code | https://github.com/plantain-00/type-coverage |
| `ts-prune` | Find unused exports | https://github.com/nadeesha/ts-prune |
| `ts-reset` | Tighter built-in types | https://github.com/total-typescript/ts-reset |
| `zod` / `valibot` / `arktype` | Runtime + static schemas | https://zod.dev |
| `tsconfig-paths` | Path alias resolution | https://github.com/dividab/tsconfig-paths |
| `eslint-plugin-total-functions` | Detect total-function violations | https://github.com/danielnixon/eslint-plugin-total-functions |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TypeScript Language Server | OSS | yes | Editor + agent in-loop diagnostics. |
| GitHub Actions | SaaS | yes | `tsc --noEmit` as required check. |
| GitLab CI / CircleCI | SaaS | yes | Same. |
| Codecov | SaaS | yes | Pair with `type-coverage --detail` for type-coverage gates. |
| `arethetypeswrong/cli` | OSS | yes | Audits dual ESM/CJS type exports. |
| Stainless / Speakeasy | SaaS | yes | Generate strictly typed SDKs from OpenAPI. |
| TypeScript Playground | SaaS | yes | Reproduce isolated type bugs with shareable URL. |
| Stryker | OSS | yes (mutation) | Mutation testing helps surface tests that don't actually exercise types. |

## Templates & scripts
See `templates.md` and `examples.md` for `tsconfig.json`, type-guard patterns, Zod boundaries. Add a strictness ratchet (≤50 lines):

```bash
#!/usr/bin/env bash
# strict-ratchet.sh — error count must not increase between runs.
# Stores baseline in .strict-baseline; run in CI on PRs.
set -euo pipefail
BASE=".strict-baseline"
COUNT=$(npx tsc --noEmit --pretty false 2>&1 | grep -c "error TS" || true)
echo "current strict errors: $COUNT"
if [ ! -f "$BASE" ]; then
  echo "$COUNT" > "$BASE"
  echo "baseline written"
  exit 0
fi
PREV=$(cat "$BASE")
if (( COUNT > PREV )); then
  echo "FAIL — strict errors increased ($PREV -> $COUNT)"
  npx tsc --noEmit --pretty false 2>&1 | grep "error TS" | head -50
  exit 1
fi
if (( COUNT < PREV )); then
  echo "$COUNT" > "$BASE"
  echo "ratchet tightened ($PREV -> $COUNT) — commit .strict-baseline"
fi
echo "OK"
```

Wire into CI; commit `.strict-baseline` decreases as a sign of progress.

## Best practices
- **`strict: true` + the four extras** (`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`, `noFallthroughCasesInSwitch`) — the canonical 2026 baseline.
- **`unknown` over `any`** at every IO boundary; convert via Zod / valibot parsers.
- **`as const` for literal preservation.** `const ROLES = ['admin','user'] as const` + `type Role = (typeof ROLES)[number]`.
- **Branded types** for IDs: `type UserId = string & { __brand: 'UserId' }`. Prevents passing OrderId where UserId expected.
- **Discriminated unions** over optional flag bags — exhaustive switch + `assertNever(x)` makes new cases fail-closed.
- **Type guards (`is X`)** colocated with the type; agents reuse them.
- **`Result<T, E>` / `Either`** at boundaries for predictable error flow; `neverthrow` library or hand-rolled.
- **`satisfies` for object literals** — ensures shape conformance without widening.
- **Path aliases (`@/`)** consistent across `tsconfig.json`, bundler, test runner. Drift = obscure module resolution errors.
- **`ts-reset`** to tighten built-ins (`JSON.parse` returns `unknown`, `.filter(Boolean)` strips falsy types).
- **Project references** for monorepos — incremental builds, type-isolation between packages.

## AI-agent gotchas
- **`as` cast as the fix-all.** Agent encounters TS error and inserts `as any` / `as unknown as Foo`. Lint rule `@typescript-eslint/no-explicit-any` + `consistent-type-assertions` catch.
- **Non-null assertion (`!`) abuse.** Agent writes `user.profile!.email`; one nullable field flushed downstream. Force agents to refactor with explicit guards.
- **`@ts-ignore` instead of `@ts-expect-error`.** Latter errors when the underlying issue is fixed; former rots silently. Prefer `expect-error` + comment + ticket.
- **Wide return types.** Agent returns `Promise<any>` from a service; consumer types collapse. Force explicit return type annotations on exported functions.
- **`Object` vs `object` vs `Record<string, unknown>`.** Agent uses `Object` (deprecated). Lint catches.
- **`Function` type.** Agent uses `cb: Function`; loses signature. Force `(x: T) => U` shapes.
- **Discriminated union without exhaustiveness check.** Agent adds new variant; old switch statement silently doesn't handle it. Force `default: assertNever(x)`.
- **`Partial<T>` everywhere.** Reduces strictness back to "everything optional". Agents reach for it instead of explicit modeling.
- **Generic constraints missing.** Agent writes `function f<T>(x: T)` then tries `x.foo`; TS errors. Adds `T extends { foo: string }` properly only when prompted.
- **Re-exporting types from JS.** Agent re-exports a runtime value as a type; bundler emits unused import. Use `import type { ... }` + `verbatimModuleSyntax`.
- **`exactOptionalPropertyTypes` surprise.** Agent writes `{ name: undefined }` to "skip" name; rejected because property-set ≠ omit. Use spread or omit explicitly.
- **`strict` flag in `extends` config.** Agent extends `@tsconfig/strictest` then overrides with `strict: false`; doesn't realize it cascades. Verify final flags via `tsc --showConfig`.
- **Type-only imports tree-shaken differently.** Agent imports a type but bundler leaves the runtime import → larger bundle. Use `import type`.
- **Zod-typed prop drilled as inferred type.** Agent passes Zod schema where consumer expects `z.infer<typeof S>`. TS error opaque; fix with `z.infer` at the boundary, not at every call site.

## References
- TypeScript Handbook — Strictness: https://www.typescriptlang.org/tsconfig#strict
- Total TypeScript: https://www.totaltypescript.com
- Matt Pocock — Beginners TypeScript Tutorial: https://www.totaltypescript.com/tutorials/beginners-typescript
- Effective TypeScript (Dan Vanderkam): https://effectivetypescript.com
- Zod docs: https://zod.dev
- ts-reset: https://github.com/total-typescript/ts-reset
- typescript-eslint: https://typescript-eslint.io
- arethetypeswrong: https://arethetypeswrong.github.io
- Sibling methodologies: `free/dev/software-developer/javascript/`, `free/dev/software-developer/error-handling/`, `free/dev/software-developer/bun-runtime/`.
